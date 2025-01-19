@echo off
echo Initializing the database...
call venv\Scripts\activate
python manage.py
echo Database initialization complete!
pause
