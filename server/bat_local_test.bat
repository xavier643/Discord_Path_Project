@echo off
setlocal

REM in server\
if not exist venv (
  python -m venv venv
)

call venv\Scripts\activate
pip install -r requirements.txt

echo Starting server at http://localhost:5000 ...
python app.py

endlocal
