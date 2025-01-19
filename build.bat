@echo off
echo Building Youth Jobs Portal Portable Package...

REM Create build directory
if exist "dist" rd /s /q "dist"
mkdir dist
mkdir dist\youth_jobs

REM Create virtual environment in the dist folder
echo Creating virtual environment...
python -m venv dist\youth_jobs\venv

REM Activate virtual environment and install requirements
call dist\youth_jobs\venv\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller

REM Copy application files
echo Copying application files...
xcopy /E /I /Y "templates" "dist\youth_jobs\templates"
xcopy /E /I /Y "static" "dist\youth_jobs\static"
xcopy /E /I /Y "migrations" "dist\youth_jobs\migrations"
xcopy /E /I /Y "docs" "dist\youth_jobs\docs"
copy "*.py" "dist\youth_jobs\"
copy "requirements.txt" "dist\youth_jobs\"
copy ".env" "dist\youth_jobs\"

REM Create startup scripts
echo Creating startup scripts...
echo @echo off > "dist\youth_jobs\start.bat"
echo call venv\Scripts\activate >> "dist\youth_jobs\start.bat"
echo python app.py >> "dist\youth_jobs\start.bat"

echo @echo off > "dist\youth_jobs\init_db.bat"
echo call venv\Scripts\activate >> "dist\youth_jobs\init_db.bat"
echo python manage.py >> "dist\youth_jobs\init_db.bat"

REM Create zip file
echo Creating zip archive...
powershell Compress-Archive -Path "dist\youth_jobs" -DestinationPath "dist\youth_jobs_portable.zip" -Force

echo Build complete! The portable package is available at dist\youth_jobs_portable.zip
pause
