@echo off
echo ========================================================
echo   eTraceAI Local Deployment ^& Internet Exposure
echo ========================================================
echo.

echo [1/3] Starting Docker containers (Frontend, Backend, Redis, ML Worker)...
call docker-compose up -d --build

echo.
echo [2/3] Checking if Node.js is installed (required for localtunnel)...
node -v >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed. Please install Node.js to expose the app to the internet.
    pause
    exit /b 1
)

echo.
echo [3/3] Exposing the application to the internet using localtunnel...
echo.
echo ========================================================
echo   SUCCESS! The tunnel will generate a public URL below.
echo   Share that URL to let anyone on the internet view
echo   the eTraceAI application.
echo.
echo   Press Ctrl+C to close the tunnel and stop sharing.
echo ========================================================
echo.

call npx -y localtunnel --port 3000
