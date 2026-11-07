@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
title GAIP-Cero-Auto - Consola en español
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
  set "PY=py -3"
) else (
  where python >nul 2>&1
  if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en PATH.
    pause
    exit /b 1
  )
  set "PY=python"
)
echo Abriendo GAIP-Cero-Auto en http://127.0.0.1:8765 ...
start "" "http://127.0.0.1:8765"
%PY% app.py
if errorlevel 1 echo ERROR: La consola terminó con un error.
pause
