@echo off
echo Packaging Youth Jobs Application...

:: Create dist directory if it doesn't exist
if not exist "dist" mkdir dist

:: Clean previous build
if exist "dist\youth_jobs" rmdir /s /q "dist\youth_jobs"
if exist "build" rmdir /s /q "build"

:: Run PyInstaller
call venv\Scripts\pyinstaller youth_jobs.spec --clean

:: Copy additional files
copy ".env" "dist\youth_jobs\.env"
copy "requirements.txt" "dist\youth_jobs\requirements.txt"
copy "start_app.bat" "dist\youth_jobs\start_app.bat"

:: Create README for deployment
echo Creating deployment instructions...
(
echo Youth Jobs Application - Deployment Package
echo =========================================
echo.
echo Requirements:
echo - Windows 10 or later
echo - Internet connection ^(for first run^)
echo.
echo Installation:
echo 1. Extract all files to a directory
echo 2. Run start_app.bat
echo.
echo Note: On first run, the application will create a new database automatically.
) > "dist\youth_jobs\README.txt"

:: Create a ZIP file
echo Creating ZIP archive...
powershell Compress-Archive -Path "dist\youth_jobs" -DestinationPath "dist\youth_jobs_portable.zip" -Force

echo.
echo Package created successfully!
echo The portable application is available in:
echo - Uncompressed: dist\youth_jobs
echo - Compressed: dist\youth_jobs_portable.zip
echo.
