#!/usr/bin/env python3
"""Deterministic samplers for cross-domain-brainstorm v0.4.

Two decks, two modes:

- Decision mode (mechanism domains): reads assets/domain-deck.json, compares the
  target's 7-axis profile with each domain, and returns a mix of high-distance
  domains, a wildcard, and (optionally) an anti-domain.
- Inspiration mode (stimulus cards): reads assets/stimulus-deck.json (100 cards
  across 11 worlds) and enforces the collision-room rules -- world coverage,
  no adjacent same-world cards, abstract floor, near-world quota, own-world ban.

Examples:
  python scripts/domain_sampler.py --target "AI note app" \
    --axis substrate=digital --axis centralization=distributed \
    --axis sync=episodic --axis risk=low --axis resource=abundant \
    --axis verification=self_reported --axis agent=individual --seed 42

  python scripts/domain_sampler.py --stimulus --target "rugged tablet" \
    --stim-count 13 --near-world workshop --ban-world "" --seed 42

  python scripts/domain_sampler.py --self-test

Pure standard library.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECK_PATH = ROOT / "assets" / "domain-deck.json"
STIMULUS_PATH = ROOT / "assets" / "stimulus-deck.json"
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
    "low_resource": "低资源",
}
EXAMPLE_IDS = {
    "er_triage",
    "nursing_handoff",
    "aviation_checklist",
    "audit",
    "immune_system",
    "monastic_office",
}
LOW_RESOURCE = {"scarce", "volatile"}

WORLDS_ZH = {
    "workshop": "工具间",
    "toybox": "玩具箱",
    "military": "军品战场",
    "biology": "生物解剖",
    "kitchen": "厨房",
    "sports": "运动",
    "farm_fishing": "农具渔猎",
    "marine_air": "航海航空",
    "medical": "医疗急救",
    "stationery_music": "文具乐器",
    "abstract_systems": "抽象制度",
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


def is_example(domain: dict) -> bool:
    return domain["id"] in EXAMPLE_IDS


def is_low_resource(domain: dict) -> bool:
    return domain["axes"]["resource"] in LOW_RESOURCE


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

    # Low-resource targets need at least one scarce/volatile domain.
    if target.get("resource") in LOW_RESOURCE and count >= 2:
        if not any(is_low_resource(item["domain"]) for item in selected):
            has_example = any(is_example(item["domain"]) for item in selected)
            pool = [
                item
                for item in remaining
                if is_low_resource(item["domain"])
                and (not has_example or not is_example(item["domain"]))
            ]
            if pool:
                for idx in range(len(selected) - 1, -1, -1):
                    if selected[idx]["role"] == "high_distance":
                        chosen = pool[0]
                        chosen["role"] = "low_resource"
                        selected[idx] = chosen
                        remaining.remove(chosen)
                        break

    # At most one example domain per sample; wildcard must not be a second example.
    if len(selected) >= 3:
        examples = [item for item in selected if is_example(item["domain"])]
        if len(examples) > 1:
            keep = max(examples, key=lambda item: item["score"])
            for item in examples:
                if item is keep:
                    continue
                pool = [
                    candidate
                    for candidate in remaining
                    if not is_example(candidate["domain"])
                ]
                if not pool:
                    break
                replacement = pool[0]
                replacement["role"] = item["role"]
                selected[selected.index(item)] = replacement
                remaining.remove(replacement)

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


def load_stimulus_deck(path: Path = STIMULUS_PATH) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        deck = json.load(fh)
    validate_stimulus_deck(deck)
    return deck


def validate_stimulus_deck(deck: dict) -> None:
    cards = deck.get("cards")
    if not isinstance(cards, list) or len(cards) != 100:
        found = len(cards) if isinstance(cards, list) else type(cards).__name__
        raise ValueError(f"stimulus deck must contain exactly 100 cards, got {found}")
    worlds = set(deck.get("worlds", []))
    if len(worlds) != 11:
        raise ValueError(f"stimulus deck must declare 11 worlds, got {len(worlds)}")
    seen_ids: set[str] = set()
    abstract = 0
    for card in cards:
        for key in ("id", "name", "world", "kind", "props", "mechanism"):
            if key not in card:
                raise ValueError(f"card missing {key!r}: {card.get('id', '?')}")
        if card["id"] in seen_ids:
            raise ValueError(f"duplicate stimulus id: {card['id']}")
        seen_ids.add(card["id"])
        if card["world"] not in worlds:
            raise ValueError(f"unknown world {card['world']!r} for {card['id']}")
        if card["kind"] not in ("concrete", "abstract"):
            raise ValueError(f"bad kind {card['kind']!r} for {card['id']}")
        if not isinstance(card["props"], list) or not card["props"]:
            raise ValueError(f"card {card['id']} needs a non-empty props list")
        abstract += 1 if card["kind"] == "abstract" else 0
    if abstract < 10:
        raise ValueError(f"stimulus deck needs >=10 abstract cards, got {abstract}")


def interleave_no_adjacent(cards: list[dict]) -> list[dict]:
    """Round-robin interleave so the same world never appears twice in a row."""
    groups: dict[str, list[dict]] = {}
    for card in cards:
        groups.setdefault(card["world"], []).append(card)
    pools = sorted(groups.values(), key=len, reverse=True)
    result: list[dict] = []
    prev_world = None
    while pools:
        idx = 0
        if pools[0] and pools[0][0]["world"] == prev_world and len(pools) > 1:
            idx = 1
        pool = pools[idx]
        card = pool.pop(0)
        result.append(card)
        prev_world = card["world"]
        pools = [p for p in pools if p]
        pools.sort(key=len, reverse=True)
    return result


def sample_stimulus(
    deck: dict,
    count: int = 13,
    seed: int = 0,
    near_world: str | None = None,
    ban_world: str | None = None,
    exclude: set[str] | None = None,
) -> list[dict]:
    """Sample stimulus cards for the collision room (inspiration mode).

    Rules enforced (v0.4):
    - the topic's own world (ban_world) is never drawn
    - a temperament-close world (near_world) gets at most max(1, count // 20) cards
    - per-world cap of count // 5 + 1 keeps >=5 worlds for Quick-size draws
    - Deep-size draws (>= 30) cover all eligible worlds
    - >= 1 abstract card (>= 3 when count >= 40); concrete dominates by deck design
    - same world never appears in adjacent positions
    """
    if count < 3:
        raise ValueError("stimulus count must be >= 3")
    all_worlds = {card["world"] for card in deck["cards"]}
    for label, world in (("ban_world", ban_world), ("near_world", near_world)):
        if world and world not in all_worlds:
            raise ValueError(f"unknown {label}: {world}; choose from {', '.join(sorted(all_worlds))}")
    exclude = set(exclude or set())
    rng = random.Random(seed)

    by_world: dict[str, list[dict]] = {}
    for card in deck["cards"]:
        if card["id"] in exclude or card["world"] == ban_world:
            continue
        by_world.setdefault(card["world"], []).append(card)
    for pool in by_world.values():
        rng.shuffle(pool)
    if sum(len(p) for p in by_world.values()) < count:
        raise ValueError(f"only {sum(len(p) for p in by_world.values())} eligible cards, requested {count}")

    near_quota = max(1, count // 20) if near_world else None
    per_world_cap = count // 5 + 1
    world_order = list(by_world)
    rng.shuffle(world_order)

    selected: list[dict] = []
    taken: dict[str, int] = {}

    def take(world: str) -> None:
        card = by_world[world].pop(0)
        selected.append(card)
        taken[world] = taken.get(world, 0) + 1

    def cap_of(world: str) -> int:
        if near_quota is not None and world == near_world:
            return near_quota
        return per_world_cap

    # Round 1: one card per world (coverage).
    for world in world_order:
        if len(selected) >= count:
            break
        if by_world[world] and taken.get(world, 0) < cap_of(world):
            take(world)

    # Round 2: fill from the largest remaining pools, respecting caps.
    guard = 0
    while len(selected) < count and guard < 10000:
        guard += 1
        progressed = False
        for world in sorted(world_order, key=lambda w: len(by_world[w]), reverse=True):
            if len(selected) >= count:
                break
            if by_world[world] and taken.get(world, 0) < cap_of(world):
                take(world)
                progressed = True
                break
        if not progressed:
            # caps exhausted: relax to hard cap of ceil(count/2) for the biggest pools
            for world in sorted(world_order, key=lambda w: len(by_world[w]), reverse=True):
                if len(selected) >= count:
                    break
                if by_world[world] and taken.get(world, 0) < (count + 1) // 2:
                    take(world)
                    progressed = True
                    break
            if not progressed:
                break

    if len(selected) < count:
        raise ValueError(f"only found {len(selected)} stimulus cards, requested {count}")

    # Abstract floor.
    abstract_floor = 3 if count >= 40 else 1
    have_abstract = sum(1 for card in selected if card["kind"] == "abstract")
    if have_abstract < abstract_floor:
        spare_abstract = [
            card
            for pool in by_world.values()
            for card in pool
            if card["kind"] == "abstract"
            and (near_quota is None or card["world"] != near_world or taken.get(card["world"], 0) < near_quota)
        ]
        rng.shuffle(spare_abstract)
        droppable = sorted(
            (i for i, card in enumerate(selected) if card["kind"] == "concrete"),
            key=lambda i: -taken.get(selected[i]["world"], 0),
        )
        for replacement in spare_abstract[: abstract_floor - have_abstract]:
            if not droppable:
                break
            idx = droppable.pop(0)
            old = selected[idx]
            taken[old["world"]] -= 1
            selected[idx] = replacement
            taken[replacement["world"]] = taken.get(replacement["world"], 0) + 1

    return interleave_no_adjacent(selected)


def render_stimulus_markdown(topic: str, cards: list[dict]) -> str:
    lines = [
        f"## 碰撞房抽牌：{topic or '(未命名题面)'}",
        "",
        "每组四行：品类[世界·具象/抽象] → 属性 → 嫁接 → 爽点。发散阶段禁词：成本/BOM/可行性/风险/认证。",
        "",
        "| # | 品类 | 世界 | 类型 | 属性 | 一句话机制 |",
        "|---|---|---|---|---|---|",
    ]
    for i, card in enumerate(cards, 1):
        lines.append(
            "| {i} | {name} | {world} | {kind} | {props} | {mech} |".format(
                i=i,
                name=card["name"],
                world=WORLDS_ZH.get(card["world"], card["world"]),
                kind="具象" if card["kind"] == "concrete" else "抽象",
                props="; ".join(card["props"]),
                mech=card["mechanism"],
            )
        )
    lines.append("")
    lines.append("弃牌要写死因；冗余测试：不用这张牌也想得出的点子不算这张牌的产出。")
    return "\n".join(lines)


def self_test() -> int:
    deck = load_deck()
    if len(deck["domains"]) != 66:
        raise AssertionError(f"expected 66 domains, got {len(deck['domains'])}")
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
    assert sum(1 for d in selected if d["id"] in EXAMPLE_IDS) <= 1, selected
    for domain in selected:
        assert len(domain["diff_axes"]) >= 3, domain
        assert domain["structural_diff"], domain
    low_target = dict(target, resource="scarce")
    low = sample(deck, low_target, count=3, seed=7)
    assert len(low) == 3, low
    assert any(d["axes"]["resource"] in LOW_RESOURCE for d in low), low
    deep = sample(deck, target, count=5, seed=42, anti_domain=True)
    assert len(deep) == 5, deep
    assert any(d["role"] == "anti_domain" for d in deep), deep

    stim = load_stimulus_deck()
    quick_cards = sample_stimulus(stim, count=13, seed=42)
    assert len(quick_cards) == 13, quick_cards
    quick_worlds = {c["world"] for c in quick_cards}
    assert len(quick_worlds) >= 5, quick_worlds
    assert sum(1 for c in quick_cards if c["kind"] == "abstract") >= 1, quick_cards
    assert sum(1 for c in quick_cards if c["kind"] == "concrete") >= 2, quick_cards
    for prev, curr in zip(quick_cards, quick_cards[1:]):
        assert prev["world"] != curr["world"], (prev["id"], curr["id"])
    deep_cards = sample_stimulus(stim, count=40, seed=7)
    assert len(deep_cards) == 40, len(deep_cards)
    assert len({c["world"] for c in deep_cards}) == 11, deep_cards
    assert sum(1 for c in deep_cards if c["kind"] == "abstract") >= 3, deep_cards
    for prev, curr in zip(deep_cards, deep_cards[1:]):
        assert prev["world"] != curr["world"], (prev["id"], curr["id"])
    tuned = sample_stimulus(stim, count=12, seed=3, near_world="military", ban_world="toybox")
    assert not any(c["world"] == "toybox" for c in tuned), tuned
    assert sum(1 for c in tuned if c["world"] == "military") <= max(1, 12 // 20), tuned
    print(
        "SELF-TEST OK: 66 domains, 3-domain Quick sample, 5-domain Deep sample, "
        "low-resource check, 100-card stimulus deck (13-quick / 40-deep / near-ban)"
    )
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
    parser.add_argument("--stimulus", action="store_true", help="sample stimulus cards (inspiration mode / collision room)")
    parser.add_argument("--stim-count", type=int, default=13, help="number of stimulus cards (default: 13; Deep: 40-60)")
    parser.add_argument("--near-world", default="", help="world id temperament-close to the topic; quota capped at max(1, count//20)")
    parser.add_argument("--ban-world", default="", help="world id matching the topic's own category; excluded entirely")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    parser.add_argument("--self-test", action="store_true", help="validate both decks and run fixed samples")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    try:
        if args.stimulus:
            deck = load_stimulus_deck()
            exclude = {item.strip() for item in args.exclude.split(",") if item.strip()}
            cards = sample_stimulus(
                deck,
                count=args.stim_count,
                seed=args.seed,
                near_world=args.near_world or None,
                ban_world=args.ban_world or None,
                exclude=exclude,
            )
        else:
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
            cards = None
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

    if args.stimulus:
        payload = cards
        text = render_stimulus_markdown(args.target, cards)
    else:
        payload = selected
        text = render_markdown(args.target, target, selected)

    if args.json:
        print(
            json.dumps(
                {"target": args.target, "seed": args.seed, "stimulus": bool(args.stimulus), "cards": payload},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
