@echo off
:: Инициализация цветов
setlocal enabledelayedexpansion

:: Цвета
set GREEN=[  OK  ]
set RED=[ FAIL ]

:: Очистка экрана
cls
echo ##########################################
echo #     ACCOUNT LOCKED COMPANY INSTALLER   #
echo ##########################################
echo.

:: 0% - Проверка Python
echo Checking for Python...
python --version >nul 2>&1
if %errorlevel%==0 (
    echo %GREEN% Python Installed.
) else (
    echo %RED% Python NOT Installed.
    pause
    exit /b
)

echo #
timeout /t 1 >nul

:: 50% - Проверка pip
echo Checking for Pip...
pip --version >nul 2>&1
if %errorlevel%==0 (
    echo %GREEN% Pip Installed.
) else (
    echo %RED% Pip NOT Installed.
    echo Installing Pip...
    python -m ensurepip
)

echo ##
timeout /t 1 >nul

:: 70% - Установка зависимостей
echo Installing requirements...
pip install -r requirements.txt
echo ###
timeout /t 1 >nul

:: 100% - Запуск приложения
echo Launching Password Safe Database...
echo ####
timeout /t 1 >nul
python P.S.B.py

echo ##########################################
echo #           PROCESS SUCCESS [100%%]       #
echo ##########################################
pause
