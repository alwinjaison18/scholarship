@echo off
echo Stopping ShikshaSetu Development Environment...
echo.

echo Stopping Docker services...
docker-compose down

echo.
echo Stopping background processes...
taskkill /f /im "python.exe" 2>nul
taskkill /f /im "node.exe" 2>nul

echo.
echo All services stopped.
pause
