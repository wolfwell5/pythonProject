@echo off
cd /d "%~dp0"
python stock\tickflowDir\scripts\BatchKlineFetcher.py
pause
