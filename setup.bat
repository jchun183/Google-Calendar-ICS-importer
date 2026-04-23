@echo off
echo Setting up "Import to Google Calendar" right-click menu...

set "BAT_PATH=%~dp0import_to_calendar.bat"
set "ICON_PATH=%~dp0calendar.ico"

reg add "HKCU\Software\Classes\SystemFileAssociations\.ics\shell\ImportToGoogleCalendar" /ve /d "Import to Google Calendar" /f
reg add "HKCU\Software\Classes\SystemFileAssociations\.ics\shell\ImportToGoogleCalendar" /v Icon /d "%ICON_PATH%,0" /f
reg add "HKCU\Software\Classes\SystemFileAssociations\.ics\shell\ImportToGoogleCalendar\command" /ve /d "\"%BAT_PATH%\" \"%%1\"" /f

echo.
echo Setup complete.
pause