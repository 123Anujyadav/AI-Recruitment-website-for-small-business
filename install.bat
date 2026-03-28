@echo off
echo Creating Virtual Environment...
python -m venv venv
call venv\Scripts\activate.bat

echo Installing Requirements...
pip install -r requirements.txt

echo Running Migrations...
python manage.py makemigrations
python manage.py makemigrations jobs
python manage.py migrate

echo Setup Complete! You can now run the app using run.bat
pause
