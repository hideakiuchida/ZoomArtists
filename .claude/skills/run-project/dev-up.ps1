# ── ZoomArtists: start infra + run migrations ───────────────────────────────
# Brings up Postgres+Redis and applies DB migrations. Then prints the two
# commands to start the backend and frontend (run those in separate terminals).

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))

Write-Host "==> Starting Postgres + Redis..." -ForegroundColor Cyan
Set-Location $root
docker compose up -d

Write-Host "==> Waiting for Postgres to be healthy..." -ForegroundColor Cyan
$tries = 0
do {
    Start-Sleep -Seconds 2
    $status = docker inspect --format='{{.State.Health.Status}}' zoomartists_postgres 2>$null
    $tries++
} while ($status -ne "healthy" -and $tries -lt 30)

if ($status -ne "healthy") {
    Write-Host "Postgres did not become healthy. Check 'docker compose ps'." -ForegroundColor Red
    exit 1
}
Write-Host "    Postgres healthy." -ForegroundColor Green

Write-Host "==> Ensuring backend/.env exists..." -ForegroundColor Cyan
$backend = Join-Path $root "backend"
if (-not (Test-Path (Join-Path $backend ".env"))) {
    Copy-Item (Join-Path $root ".env.example") (Join-Path $backend ".env")
    Write-Host "    Created backend/.env from .env.example" -ForegroundColor Green
}

Write-Host "==> Running migrations..." -ForegroundColor Cyan
Set-Location $backend
$versions = Join-Path $backend "alembic\versions"
$hasMigrations = (Test-Path $versions) -and ((Get-ChildItem $versions -Filter *.py -ErrorAction SilentlyContinue).Count -gt 0)
if (-not $hasMigrations) {
    Write-Host "    No migrations found, generating initial schema..." -ForegroundColor Yellow
    uv run alembic revision --autogenerate -m "initial schema"
}
uv run alembic upgrade head

Write-Host ""
Write-Host "Infra ready. Now start the servers in two terminals:" -ForegroundColor Green
Write-Host "  Backend : cd backend; uv run uvicorn app.main:app --reload --port 8000"
Write-Host "  Frontend: cd frontend; npm start"
Write-Host ""
Write-Host "Then open http://localhost:4200" -ForegroundColor Cyan
