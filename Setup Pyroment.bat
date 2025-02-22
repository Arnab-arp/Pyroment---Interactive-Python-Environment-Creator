@echo off
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is NOT installed.
    powershell -Command "& {Add-Type –TypeDefinition 'using System.Windows.Forms; public class MsgBox { public static void Show(string msg) { MessageBox.Show(msg, \"Error\", 'OK', 'Error'); }}'; [MsgBox]::Show('Python is not installed on this system.')}"
    exit /b 1
) else (
    echo -------------------------------------------
    echo.
    echo Running On Python
    python --version
    echo.
    echo Required Packages Needed To Be Installed
    echo [mypy, tk-tools, prettytable]
    echo.
    echo -------------------------------------------
    pause
    pip install prettytable
    pip install tk-tools
)
pause