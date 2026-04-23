@echo off
echo Setting up "Import to Google Calendar" right-click menu for current user...

set "BAT_PATH=%~dp0import_to_calendar.bat"

reg add "HKCU\Software\Classes\SystemFileAssociations\.ics\shell\ImportToGoogleCalendar" /ve /d "Import to Google Calendar" /f
reg add "HKCU\Software\Classes\SystemFileAssociations\.ics\shell\ImportToGoogleCalendar\command" /ve /d "\"%BAT_PATH%\" \"%%1\"" /f

echo.
echo Setup complete.
echo If you do not see it immediately, close and reopen File Explorer.
pause