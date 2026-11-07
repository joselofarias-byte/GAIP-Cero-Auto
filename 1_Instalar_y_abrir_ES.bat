@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
title GAIP-Cero-Auto - Instalación y consola
echo ==============================================================
echo    GAIP-Cero-Auto - Primera ejecución en español
echo ==============================================================
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
  set "PY=py -3"
) else (
  where python >nul 2>&1
  if errorlevel 1 (
    echo ERROR: No se encontró Python. Instalá Python 3.10 o superior.
    pause
    exit /b 1
  )
  set "PY=python"
)
echo Instalando las dependencias de Python...
%PY% -m pip install -r requirements.txt
if errorlevel 1 (
  echo ERROR: No se pudieron instalar las dependencias.
  pause
  exit /b 1
)
echo Instalando Chromium requerido por Playwright...
%PY% -m playwright install chromium
if errorlevel 1 (
  echo ERROR: No se pudo instalar Chromium de Playwright.
  pause
  exit /b 1
)
echo Abriendo panel local http://127.0.0.1:8765 ...
start "" "http://127.0.0.1:8765"
%PY% app.py
if errorlevel 1 echo ERROR: El servidor terminó con un error.
pause
