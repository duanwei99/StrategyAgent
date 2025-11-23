# Download Freqtrade Data with Proxy
# PowerShell Script

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Download Data with Proxy" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# ============================================
# Configure your proxy here
# ============================================
$PROXY_HOST = "127.0.0.1"
$PROXY_PORT = "10808"
# ============================================

$env:HTTP_PROXY = "http://${PROXY_HOST}:${PROXY_PORT}"
$env:HTTPS_PROXY = "http://${PROXY_HOST}:${PROXY_PORT}"

Write-Host "Current Proxy Settings:" -ForegroundColor Yellow
Write-Host "  HTTP_PROXY: $env:HTTP_PROXY"
Write-Host "  HTTPS_PROXY: $env:HTTPS_PROXY"
Write-Host ""

Write-Host "Starting download..." -ForegroundColor Green
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
    Write-Host "[FAILED] Download failed even with proxy" -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Suggestions:" -ForegroundColor Yellow
    Write-Host "  1. Check if proxy is running at ${PROXY_HOST}:${PROXY_PORT}"
    Write-Host "  2. Try different proxy port"
    Write-Host "  3. Use simulation mode"
    Write-Host ""
} else {
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
}

Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

