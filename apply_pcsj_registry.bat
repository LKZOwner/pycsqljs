@echo off
echo Applying PyCppSQLJS file type registration...
regedit /s register_pcsj.reg
echo Registry changes applied.
echo.
echo Restarting Windows Explorer...
taskkill /f /im explorer.exe
start explorer.exe
echo.
echo Done! The .pcsj file type should now be properly registered.
echo Please try opening a .pcsj file to verify the registration.
pause 