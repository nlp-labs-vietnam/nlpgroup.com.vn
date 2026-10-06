@echo off
title nlpgroup.com.vn - Dev Server
color 0A
echo.
echo  ================================================
echo   nlpgroup.com.vn  ^|  Dev Server
echo  ================================================
echo.
echo  Dang kiem tra Node.js va npm...
where node >nul 2>&1 || (echo  [LOI] Node.js chua duoc cai dat! && pause && exit /b 1)
where npm  >nul 2>&1 || (echo  [LOI] npm chua duoc cai dat!    && pause && exit /b 1)
echo  [OK] Node.js: && node -v
echo  [OK] npm:     && npm -v
echo.
echo  Kiem tra node_modules...
if not exist "node_modules" (
    echo  [INFO] Chua co node_modules - dang cai dat...
    npm install
    echo.
)
echo  Khoi dong dev server tai http://localhost:3000
echo  Nhan Ctrl+C de dung server.
echo.
npm start
pause
