@echo off
REM eTraceAI Deployment Script for Windows
REM This script simplifies the deployment process

setlocal enabledelayedexpansion

echo ============================================
echo   eTraceAI Docker Deployment Script
echo ============================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo [SUCCESS] Docker and Docker Compose are installed
echo.

REM Create necessary directories
echo [INFO] Creating necessary directories...
if not exist "data" mkdir data
if not exist "output" mkdir output
if not exist "reference_db" mkdir reference_db
if not exist "models" mkdir models

:menu
echo.
echo Select an option:
echo 1) Build and start the application
echo 2) Start the application (existing build)
echo 3) Stop the application
echo 4) View logs
echo 5) Restart the application
echo 6) Clean up (remove containers and images)
echo 7) Exit
echo.

set /p choice="Enter your choice [1-7]: "

if "%choice%"=="1" goto build
if "%choice%"=="2" goto start
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto logs
if "%choice%"=="5" goto restart
if "%choice%"=="6" goto cleanup
if "%choice%"=="7" goto exit
goto invalid

:build
echo [INFO] Building and starting eTraceAI...
docker-compose up --build -d
if %errorlevel% equ 0 (
    echo [SUCCESS] eTraceAI is now running!
    echo [INFO] Access the application at: http://localhost:8501
) else (
    echo [ERROR] Failed to build and start the application
)
goto menu

:start
echo [INFO] Starting eTraceAI...
docker-compose up -d
if %errorlevel% equ 0 (
    echo [SUCCESS] eTraceAI is now running!
    echo [INFO] Access the application at: http://localhost:8501
) else (
    echo [ERROR] Failed to start the application
)
goto menu

:stop
echo [INFO] Stopping eTraceAI...
docker-compose down
if %errorlevel% equ 0 (
    echo [SUCCESS] eTraceAI has been stopped
) else (
    echo [ERROR] Failed to stop the application
)
goto menu

:logs
echo [INFO] Displaying logs (Press Ctrl+C to exit)...
docker-compose logs -f
goto menu

:restart
echo [INFO] Restarting eTraceAI...
docker-compose restart
if %errorlevel% equ 0 (
    echo [SUCCESS] eTraceAI has been restarted
) else (
    echo [ERROR] Failed to restart the application
)
goto menu

:cleanup
echo [WARNING] This will remove all containers and images. Are you sure? (Y/N)
set /p confirm="Enter your choice: "
if /i "%confirm%"=="Y" (
    echo [INFO] Cleaning up...
    docker-compose down -v
    docker rmi etraceai-etraceai 2>nul
    echo [SUCCESS] Cleanup complete
) else (
    echo [INFO] Cleanup cancelled
)
goto menu

:invalid
echo [ERROR] Invalid option. Please try again.
goto menu

:exit
echo [INFO] Exiting...
exit /b 0
