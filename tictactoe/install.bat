@echo off
echo === Dang cai dat cac thu vien Python ===

:: Kiem tra pip
python -m ensurepip --default-pip

:: Cai dat cac thu vien tu requirements.txt
pip install -r requirements.txt

echo === Cai dat hoan tat ===
pause
