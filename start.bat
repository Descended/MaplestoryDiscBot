:: This script allows the user to launch the bot without needing to learn command line
:: This script allows the user to choose between global and virtual python environment
:: Turn ECHO off
@echo off
setlocal
:: Turn ECHO on
:: echo on

echo "This script will launch the Discord bot."
echo "Please select the environment to run the source code with:"
echo "A: Virtual Python Environment"
echo "B: Global Python Environment"
choice /c AB /t 10 /d A /m "What is your choice"
if errorlevel 1 call :virtual
if errorlevel 2 call :global
:: Turn ECHO off
:: @echo off
pause
endlocal

:: function to run from venv
:virtual
echo "You have selected A: Virtual Python Environment"
call venv\scripts\activate.bat
venv\scripts\python src/main.py
:: echo "The bot crashed, restarting bot.."
:: goto virtual
EXIT /B 0

:: function to run from global environment
:global
echo "You have selected B: Global Python Environment"
python src/main.py
:: echo "The bot crashed, restarting bot.."
:: goto global
EXIT /B 0
