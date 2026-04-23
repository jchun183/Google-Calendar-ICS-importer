@echo off
echo Setting up "Import to Google Calendar" right-click menu...

set "EXE_PATH=%~dp0CalendarImporter.exe"
set "ICON_PATH=%~dp0calendar.ico"

reg add "HKCU\Software\Classes\SystemFileAssociations\.ics\shell\ImportToGoogleCalendar" /ve /d "Import to Google Calendar" /f
reg add "HKCU\Software\Classes\SystemFileAssociations\.ics\shell\ImportToGoogleCalendar" /v Icon /d "%ICON_PATH%,0" /f
reg add "HKCU\Software\Classes\SystemFileAssociations\.ics\shell\ImportToGoogleCalendar\command" /ve /d "\"%EXE_PATH%\" \"%%1\"" /f

echo.
echo Setup complete.
pause