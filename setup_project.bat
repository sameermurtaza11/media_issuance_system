@echo off
echo --- Cloning the repository ---
git clone https://github.com/sameermurtaza11/media_issuance_system.git
cd media_issuance_system

echo --- Creating virtual environment ---
python -m venv venv

echo --- Activating virtual environment ---
call venv\Scripts\activate

echo --- Installing required libraries ---
pip install -r requirements.txt

echo --- Running the Flask server ---
python app.py

pause
