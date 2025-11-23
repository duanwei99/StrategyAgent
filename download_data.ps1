# Download Freqtrade Data (No Proxy)
# PowerShell Script

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Download Freqtrade Historical Data" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[INFO] This script will download:" -ForegroundColor Yellow
Write-Host "  - Exchange: OKX"
Write-Host "  - Pairs: BTC/USDT, ETH/USDT"
Write-Host "  - Time Range: January 2023 (1 month)"
Write-Host "  - Timeframe: 5 minutes"
Write-Host "  - Estimated Size: ~10 MB"
Write-Host "  - Estimated Time: 2-5 minutes"
Write-Host ""

$confirm = Read-Host "Continue download? (y/N)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Cancelled."
    exit 0
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "Starting download..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# Activate conda environment
& conda activate quant

# Change to freqtrade directory
Push-Location freqtrade_worker

# Download data
& freqtrade download-data `
    --exchange okx `
    --pairs BTC/USDT ETH/USDT `
    --timerange 20230101-20230131 `
    --timeframe 5m `
    --config user_data/config.json `
    --userdir user_data

$exitCode = $LASTEXITCODE

# Return to original directory
Pop-Location

if ($exitCode -ne 0) {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Red
    Write-Host "[ERROR] Data download failed!" -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possible causes:" -ForegroundColor Yellow
    Write-Host "  1. Cannot connect to OKX API (network/firewall issue)"
    Write-Host "  2. API rate limit"
    Write-Host "  3. Incorrect pair names"
    Write-Host ""
    Write-Host "Solutions:" -ForegroundColor Yellow
    Write-Host "  1. Check network connection"
    Write-Host "  2. Use proxy version: .\download_data_proxy.ps1"
    Write-Host "  3. Try again later"
    Write-Host "  4. Use simulation mode (auto-enabled)"
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "[SUCCESS] Data downloaded successfully!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Data location: freqtrade_worker\user_data\data\okx\"
Write-Host ""

if (Test-Path "freqtrade_worker\user_data\data\okx\") {
    Write-Host "Files:"
    Get-ChildItem "freqtrade_worker\user_data\data\okx\*.json" -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "  - $($_.Name)" }
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Restart backend service (if running)"
Write-Host "  2. Now you can backtest with real data!"
Write-Host ""

Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

