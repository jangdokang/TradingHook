call python -m venv .venv
call .venv\Scripts\activate.bat
call .venv\Scripts\python.exe -m pip install --upgrade pip
call pip install -r requirements.txt
pause