# nlpgroup.com.vn - Dev Server Launcher
# Chay: .\start-dev.ps1

$host.UI.RawUI.WindowTitle = "nlpgroup.com.vn - Dev Server"
Write-Host ""
Write-Host "  ================================================" -ForegroundColor Cyan
Write-Host "   nlpgroup.com.vn  |  Dev Server" -ForegroundColor Cyan
Write-Host "  ================================================" -ForegroundColor Cyan
Write-Host ""

# Kiem tra Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "  [LOI] Node.js chua duoc cai dat!" -ForegroundColor Red
    Write-Host "  Tai ve tai: https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "Nhan Enter de thoat"
    exit 1
}
$nodeVer = node -v
$npmVer  = npm -v
Write-Host "  [OK] Node.js: $nodeVer" -ForegroundColor Green
Write-Host "  [OK] npm:     $npmVer"  -ForegroundColor Green
Write-Host ""

# Kiem tra node_modules
if (-not (Test-Path "node_modules")) {
    Write-Host "  [INFO] Chua co node_modules - dang cai dat..." -ForegroundColor Yellow
    npm install
    Write-Host ""
}

Write-Host "  Khoi dong dev server..." -ForegroundColor Cyan
Write-Host "  URL: http://localhost:3000" -ForegroundColor White
Write-Host "  Nhan Ctrl+C de dung server." -ForegroundColor Gray
Write-Host ""

npm start
