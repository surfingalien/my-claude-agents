param(
    [string[]]$TargetDirs = @(
        "$env:USERPROFILE\.github\agents",
        "$env:USERPROFILE\.copilot\agents",
        "$env:USERPROFILE\.claude\agents"
    )
)

# Localize agent name/description fields to Chinese.
# Uses agent-names-zh.json as the lookup table.
# Matches on the agent's English 'name' field in YAML frontmatter.
#
# Usage:
#   .\scripts\localize-agents-zh.ps1
#   .\scripts\localize-agents-zh.ps1 -TargetDirs "$env:USERPROFILE\.claude\agents"
#
# After running, reload VS Code (Ctrl+Shift+P -> Reload Window) to apply.

$mapFile = Join-Path $PSScriptRoot "agent-names-zh.json"
if (-not (Test-Path $mapFile)) {
    Write-Error "agent-names-zh.json not found at $mapFile"
    exit 1
}

$map = Get-Content $mapFile -Raw -Encoding UTF8 | ConvertFrom-Json

$totalUpdated = 0
foreach ($dir in $TargetDirs) {
    if (-not (Test-Path $dir)) {
        Write-Warning "Skip (not found): $dir"
        continue
    }

    $files = Get-ChildItem "$dir\*.md" -ErrorAction SilentlyContinue
    $updated = 0

    foreach ($f in $files) {
        $raw = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)

        # Must start with YAML frontmatter
        if (-not $raw.StartsWith("---")) { continue }
        $endIdx = $raw.IndexOf("---", 3)
        if ($endIdx -lt 0) { continue }

        $yaml = $raw.Substring(3, $endIdx - 3)

        # Extract current name field
        if (-not ($yaml -match "(?m)^name:\s*(.+)$")) { continue }
        $currentName = $Matches[1].Trim()

        # Look up Chinese translation
        $entry = $map.$currentName
        if (-not $entry) { continue }

        # Replace name and description in YAML
        $newYaml = $yaml -replace "(?m)^name:\s*.+$", "name: $($entry.name)"
        if ($newYaml -match "(?m)^description:") {
            $newYaml = $newYaml -replace "(?m)^description:\s*.+$", "description: $($entry.description)"
        }

        $newContent = "---" + $newYaml + "---" + $raw.Substring($endIdx + 3)
        [System.IO.File]::WriteAllText($f.FullName, $newContent, [System.Text.Encoding]::UTF8)
        $updated++

        Write-Host "  Localized: $($f.Name) -> $($entry.name)"
    }

    Write-Host "OK: $updated agents localized -> $dir"
    $totalUpdated += $updated
}

Write-Host ""
Write-Host "Total: $totalUpdated agent files updated."
Write-Host "Reload VS Code window (Ctrl+Shift+P -> Reload Window) to apply changes."
