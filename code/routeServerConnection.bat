@echo off
setlocal enabledelayedexpansion

set "RouteConnServer=192.168.100.202" :: Change value of server by name/ip

:: Each version different Kasperskey Lab character
set "kaspersky_paths[1]=C:\Program Files (x86)\Kaspersky Lab\NetworkAgent\"
set "kaspersky_paths[2]=C:\Program Files (x86)\KasperskyLab\NetworkAgent\"

:: Check if the script is running with administrative privileges
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system" && (
    set "kaspersky_found="
    for %%a in (1 2) do (
        IF EXIST "!kaspersky_paths[%%a]!" (
            set "kaspersky_path=!kaspersky_paths[%%a]!"
            set "kaspersky_found=1"
            goto :ExecuteRouteConnection
        )
    )
    if not defined kaspersky_found (
        echo Error - The folder NetworkAgent does not exist and please Inform the administrator
        pause
    )
    :ExecuteRouteConnection
    "!kaspersky_path!klmover.exe" -address "%RouteConnServer%"
    echo ----------------completed--------------------
    pause
) || (
    echo Please run this script as an administrator
    pause
)
