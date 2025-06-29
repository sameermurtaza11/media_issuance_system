@echo off
echo [1/4] Activating virtual environment...
call venv\Scripts\activate

echo [2/4] Checking and setting up database...
python init_db.py

echo [3/4] Starting Flask server...
start cmd /k "python app.py"

echo [4/4] Opening index.html in browser...
start index.html

exit
