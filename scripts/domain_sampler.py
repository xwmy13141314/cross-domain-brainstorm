#!/usr/bin/env python3
"""Deterministic domain sampler for cross-domain-brainstorm v0.2.

Reads assets/domain-deck.json, compares the target's 7-axis profile with each
domain, and returns a mix of high-distance domains, a wildcard, and (optionally)
an anti-domain. Pure standard library.

Examples:
  python scripts/domain_sampler.py --target "AI note app" \
    --axis substrate=digital --axis centralization=distributed \
    --axis sync=episodic --axis risk=low --axis resource=abundant \
    --axis verification=self_reported --axis agent=individual --seed 42

  python scripts/domain_sampler.py --self-test
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECK_PATH = ROOT / "assets" / "domain-deck.json"
AXES = (
    "substrate",
    "centralization",
    "sync",
    "risk",
    "resource",
    "verification",
    "agent",
)
STRUCTURAL = ("centralization", "sync", "verification")
RICHNESS_SCORE = {"high": 3, "medium": 2, "low": 1}
ROLE_LABEL = {
    "high_distance": "高距离",
    "wildcard": "wildcard",
    "anti_domain": "anti-domain",
}


def load_deck(path: Path = DECK_PATH) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        deck = json.load(fh)
    validate_deck(deck)
    return deck


def validate_deck(deck: dict) -> None:
    if not isinstance(deck.get("domains"), list) or not deck["domains"]:
        raise ValueError("deck must contain a non-empty 'domains' list")
    allowed = deck.get("axes", {})
    seen_ids: set[str] = set()
    seen_names: set[str] = set()
    for domain in deck["domains"]:
        for key in ("id", "name", "family", "axes", "mechanisms", "richness"):
            if key not in domain:
                raise ValueError(f"domain missing {key!r}: {domain.get('id', '?')}")
        if domain["id"] in seen_ids:
            raise ValueError(f"duplicate id: {domain['id']}")
        if domain["name"] in seen_names:
            raise ValueError(f"duplicate name: {domain['name']}")
        seen_ids.add(domain["id"])
        seen_names.add(domain["name"])
        if domain["richness"] not in RICHNESS_SCORE:
            raise ValueError(f"bad richness for {domain['id']}: {domain['richness']}")
        for axis in AXES:
            value = domain["axes"].get(axis)
            if axis not in allowed or value not in allowed[axis]:
                raise ValueError(f"bad axis {axis}={value!r} for {domain['id']}")


def parse_axes(pairs: list[str]) -> dict[str, str]:
    target: dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"axis must be key=value, got: {pair}")
        key, value = pair.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key not in AXES:
            raise ValueError(f"unknown axis: {key}; choose from {', '.join(AXES)}")
        target[key] = value
    return target


def axis_diffs(target: dict[str, str], domain: dict) -> tuple[list[str], list[str]]:
    diffs = [axis for axis in AXES if axis in target and target[axis] != domain["axes"][axis]]
    structural = [axis for axis in STRUCTURAL if axis in diffs]
    return diffs, structural


def base_score(target: dict[str, str], domain: dict) -> float:
    diffs, structural = axis_diffs(target, domain)
    return len(diffs) * 2 + len(structural) * 3 + RICHNESS_SCORE[domain["richness"]]


def is_anti_domain(target: dict[str, str], domain: dict) -> bool:
    """At least two of the three structural axes point the opposite way."""
    checks = [
        target.get("centralization") and domain["axes"]["centralization"] != target["centralization"],
        target.get("sync") and domain["axes"]["sync"] != target["sync"],
        target.get("verification") and domain["axes"]["verification"] != target["verification"],
    ]
    return sum(1 for check in checks if check) >= 2


def sample(
    deck: dict,
    target: dict[str, str],
    count: int = 3,
    seed: int = 0,
    wildcard: int = 1,
    anti_domain: bool = False,
    exclude: set[str] | None = None,
) -> list[dict]:
    if count < 1:
        raise ValueError("count must be >= 1")
    if wildcard < 0:
        raise ValueError("wildcard must be >= 0")
    exclude = exclude or set()
    rng = random.Random(seed)

    candidates = []
    for domain in deck["domains"]:
        if domain["id"] in exclude:
            continue
        diffs, structural = axis_diffs(target, domain)
        if len(diffs) < 3 or not structural:
            continue
        score = base_score(target, domain) + rng.random() * 0.5
        candidates.append(
            {
                "domain": domain,
                "score": score,
                "diffs": diffs,
                "structural": structural,
                "role": "high_distance",
            }
        )

    if not candidates:
        raise ValueError(
            "no domain is >=3 axes away with >=1 structural difference; "
            "relax the target profile or add domains to the deck"
        )

    candidates.sort(key=lambda item: item["score"], reverse=True)
    special = wildcard + (1 if anti_domain else 0)
    base_n = max(0, count - special)
    selected = candidates[:base_n]
    remaining = [item for item in candidates if item not in selected]

    def take(predicate, role: str) -> None:
        if not remaining:
            return
        pool = [item for item in remaining if predicate(item)]
        if not pool:
            pool = remaining
        pool.sort(key=lambda item: item["score"], reverse=True)
        chosen = pool[0]
        chosen["role"] = role
        selected.append(chosen)
        remaining.remove(chosen)

    for _ in range(wildcard):
        take(lambda item: item["domain"]["axes"]["substrate"] != target.get("substrate"), "wildcard")

    if anti_domain:
        take(lambda item: is_anti_domain(target, item["domain"]), "anti_domain")

    # Fill any shortfall (e.g. count > candidates) without failing silently.
    while len(selected) < count and remaining:
        chosen = remaining.pop(0)
        chosen["role"] = "high_distance"
        selected.append(chosen)

    if len(selected) < count:
        raise ValueError(f"only found {len(selected)} domains, requested {count}")

    for item in selected:
        item["domain"] = dict(item["domain"])
        item["domain"]["role"] = item["role"]
        item["domain"]["diff_axes"] = item["diffs"]
        item["domain"]["structural_diff"] = item["structural"]
        item["domain"]["score"] = round(item["score"], 2)
    return [item["domain"] for item in selected]


def render_markdown(target_name: str, target: dict[str, str], selected: list[dict]) -> str:
    lines = [
        f"## Sampled domains: {target_name or '(unnamed target)'}",
        "",
        f"Target axes: {', '.join(f'{k}={v}' for k, v in target.items())}",
        "",
        "| Role | Domain | Family | Diff axes | Structural diff | Richness | Bridge hint | Mechanisms |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for domain in selected:
        lines.append(
            "| {role} | {name} | {family} | {diffs} | {structural} | {richness} | {bridge} | {mechanisms} |".format(
                role=ROLE_LABEL.get(domain["role"], domain["role"]),
                name=domain["name"],
                family=domain["family"],
                diffs=", ".join(domain["diff_axes"]),
                structural=", ".join(domain["structural_diff"]),
                richness=domain["richness"],
                bridge=domain["bridge_hint"],
                mechanisms="; ".join(domain["mechanisms"]),
            )
        )
    lines.append("")
    lines.append("Before using a domain, write the structural bridge and the mechanism's failure precondition.")
    return "\n".join(lines)


def self_test() -> int:
    deck = load_deck()
    if len(deck["domains"]) != 48:
        raise AssertionError(f"expected 48 domains, got {len(deck['domains'])}")
    target = {
        "substrate": "digital",
        "centralization": "distributed",
        "sync": "episodic",
        "risk": "low",
        "resource": "abundant",
        "verification": "self_reported",
        "agent": "individual",
    }
    selected = sample(deck, target, count=3, seed=42)
    assert len(selected) == 3, selected
    assert any(d["role"] == "wildcard" for d in selected), selected
    for domain in selected:
        assert len(domain["diff_axes"]) >= 3, domain
        assert domain["structural_diff"], domain
    deep = sample(deck, target, count=5, seed=42, anti_domain=True)
    assert len(deep) == 5, deep
    assert any(d["role"] == "anti_domain" for d in deep), deep
    print("SELF-TEST OK: 48 domains, 3-domain Quick sample, 5-domain Deep sample")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default="", help="display name of the target")
    parser.add_argument("--axis", action="append", default=[], metavar="KEY=VALUE", help="target axis value; repeatable")
    parser.add_argument("--seed", type=int, default=0, help="deterministic seed (default: 0)")
    parser.add_argument("--count", type=int, default=3, help="number of domains (default: 3)")
    parser.add_argument("--wildcard", type=int, default=1, help="wildcard slots (default: 1)")
    parser.add_argument("--anti-domain", action="store_true", help="include one anti-domain slot (Deep mode)")
    parser.add_argument("--exclude", default="", help="comma-separated domain ids to exclude")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    parser.add_argument("--self-test", action="store_true", help="validate the deck and run fixed samples")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    try:
        target = parse_axes(args.axis)
        if len(target) < 3 or not any(axis in target for axis in STRUCTURAL):
            raise ValueError(
                "provide at least 3 axes, including one structural axis "
                "(centralization, sync, or verification)"
            )
        deck = load_deck()
        for axis, value in target.items():
            allowed = deck["axes"].get(axis, [])
            if value not in allowed:
                raise ValueError(
                    f"axis {axis}={value!r} is not in the deck; choose from {', '.join(allowed)}"
                )
        exclude = {item.strip() for item in args.exclude.split(",") if item.strip()}
        selected = sample(
            deck,
            target,
            count=args.count,
            seed=args.seed,
            wildcard=args.wildcard,
            anti_domain=args.anti_domain,
            exclude=exclude,
        )
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(
            json.dumps(
                {"target": args.target, "axes": target, "seed": args.seed, "domains": selected},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(render_markdown(args.target, target, selected))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
