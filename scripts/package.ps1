<#
.SYNOPSIS
  Build cross-domain-brainstorm.zip from the skill source.
.DESCRIPTION
  Creates a clean staging folder, copies the skill payload, removes caches, and
  writes the zip at the repository root. Run from anywhere:
    pwsh -NoProfile -File scripts/package.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$out = Join-Path $root 'cross-domain-brainstorm.zip'
$staging = Join-Path ([System.IO.Path]::GetTempPath()) ('cdb-package-' + [guid]::NewGuid().ToString('N'))
$pkg = Join-Path $staging 'cross-domain-brainstorm'

try {
    New-Item -ItemType Directory -Path $pkg -Force | Out-Null

    $files = @('SKILL.md', 'README.md', 'CHANGELOG.md', 'CONTRIBUTING.md', 'LICENSE', '.gitignore', '.markdownlint.json', '.markdownlintignore')
    foreach ($file in $files) {
        $source = Join-Path $root $file
        if (Test-Path $source) {
            Copy-Item -LiteralPath $source -Destination $pkg
        }
    }

    $dirs = @('references', 'assets', 'scripts', 'evals', '.github')
    foreach ($dir in $dirs) {
        $source = Join-Path $root $dir
        if (Test-Path $source) {
            Copy-Item -LiteralPath $source -Destination $pkg -Recurse
        }
    }

    Get-ChildItem -LiteralPath $pkg -Recurse -Directory -Filter '__pycache__' -ErrorAction SilentlyContinue |
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

    if (Test-Path $out) {
        Remove-Item -LiteralPath $out -Force
    }
    Compress-Archive -Path $pkg -DestinationPath $out -CompressionLevel Optimal
    $size = [math]::Round((Get-Item -LiteralPath $out).Length / 1KB, 1)
    Write-Host "Packaged $out ($size KB)"
}
finally {
    if (Test-Path $staging) {
        Remove-Item -LiteralPath $staging -Recurse -Force -ErrorAction SilentlyContinue
    }
}
