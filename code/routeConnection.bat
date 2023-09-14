@echo off
:: Check if the script is running with administrative privileges
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system" && (
    IF EXIST "C:\Program Files (x86)\Kaspersky Lab\NetworkAgent\klmover.exe" (
        "C:\Program Files (x86)\Kaspersky Lab\NetworkAgent\klmover.exe" -address 192.168.10.202
    pause
    )  else (
        echo Error - The file "klmover.exe" does not exist.
        pause
    )
) || (
    echo Please run this script as an administrator
    pause
)
