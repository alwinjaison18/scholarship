@echo off
echo Starting ShikshaSetu Development Environment...
echo.

:: Check if Docker is running
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

echo 1. Starting database and Redis services...
docker-compose up -d postgres redis

echo.
echo 2. Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo.
echo 3. Installing Python dependencies...
cd backend
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate
pip install -r requirements.txt

echo.
echo 4. Installing Playwright browsers...
playwright install

echo.
echo 5. Starting FastAPI backend...
start "Backend" cmd /k "call venv\Scripts\activate && python main.py"

cd ..

echo.
echo 6. Installing Node.js dependencies...
npm install

echo.
echo 7. Starting Next.js frontend...
start "Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo ShikshaSetu is starting up!
echo ========================================
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to view services status...
pause >nul

echo.
echo Checking services...
echo.
echo Docker services:
docker-compose ps

echo.
echo To stop all services, run: stop-project.bat
echo.
pause
