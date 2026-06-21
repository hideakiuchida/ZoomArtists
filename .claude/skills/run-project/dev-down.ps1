# ── ZoomArtists: stop infra ──────────────────────────────────────────────────
# Stops Postgres + Redis containers. Pass -Wipe to also delete the DB volume.

param([switch]$Wipe)

$root = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
Set-Location $root

if ($Wipe) {
    Write-Host "==> Stopping containers AND wiping database volume..." -ForegroundColor Yellow
    docker compose down -v
} else {
    Write-Host "==> Stopping containers (database preserved)..." -ForegroundColor Cyan
    docker compose down
}

Write-Host "Done. Stop the backend/frontend terminals manually (Ctrl+C)." -ForegroundColor Green
