# One-click local runner for the Event-Driven + API Gateway prototype.
# Uses the project's .venv directly (no activation needed) and auto-selects free
# ports so it never collides with other servers you may have running.
#
# Usage:  right-click > Run with PowerShell, OR:
#   powershell -ExecutionPolicy Bypass -File .\run_local.ps1

$ErrorActionPreference = "Stop"
$proto = $PSScriptRoot
$repo  = Split-Path $proto -Parent
$vpy   = Join-Path $repo ".venv\Scripts\python.exe"

if (-not (Test-Path $vpy)) {
    Write-Host "venv not found at $vpy" -ForegroundColor Red
    Write-Host "Create it first:  py -m venv .venv ; then install deps." -ForegroundColor Yellow
    exit 1
}

function Find-FreePort([int]$start) {
    for ($p = $start; $p -lt ($start + 50); $p++) {
        $busy = Get-NetTCPConnection -State Listen -LocalPort $p -ErrorAction SilentlyContinue
        if (-not $busy) { return $p }
    }
    throw "no free port near $start"
}

$recoPort = Find-FreePort 8001
$gwPort   = Find-FreePort 8000
if ($gwPort -eq $recoPort) { $gwPort = Find-FreePort ($recoPort + 1) }

Write-Host "Internal recommendation service -> http://127.0.0.1:$recoPort" -ForegroundColor Cyan
Write-Host "Public API gateway              -> http://127.0.0.1:$gwPort"   -ForegroundColor Cyan

# Start the internal service (its own window so you can see logs / Ctrl+C to stop)
Start-Process powershell -ArgumentList @(
    "-NoExit","-Command",
    "cd '$proto'; & '$vpy' -m uvicorn recommendation_api:app --host 127.0.0.1 --port $recoPort"
)

# Gateway must know where the internal service is
$env:RECO_SERVICE = "http://127.0.0.1:$recoPort"
Start-Process powershell -ArgumentList @(
    "-NoExit","-Command",
    "`$env:RECO_SERVICE='http://127.0.0.1:$recoPort'; cd '$proto'; & '$vpy' -m uvicorn api_gateway:app --host 127.0.0.1 --port $gwPort"
)

# Wait for the gateway to come up
$up = $false
for ($i = 0; $i -lt 40; $i++) {
    try { Invoke-RestMethod "http://127.0.0.1:$gwPort/health" -TimeoutSec 1 | Out-Null; $up = $true; break }
    catch { Start-Sleep -Milliseconds 500 }
}

if ($up) {
    Write-Host "`nGateway is up. Opening API docs..." -ForegroundColor Green
    Start-Process "http://127.0.0.1:$gwPort/docs"
    Write-Host "`nSend the demo events + get recommendations:" -ForegroundColor Yellow
    Write-Host "  `$env:GATEWAY_URL='http://127.0.0.1:$gwPort'; & '$vpy' '$proto\demo_requests.py'"
    Write-Host "`nInternal service docs: http://127.0.0.1:$recoPort/docs"
    Write-Host "Stop the servers by closing the two PowerShell windows that opened."
} else {
    Write-Host "Gateway did not respond in time - check the two server windows for errors." -ForegroundColor Red
}
