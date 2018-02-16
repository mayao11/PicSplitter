pyinstaller TkPicSplitter.py --add-data "C:\Python36\tcl\tkdnd2.8";"tcl" -F
if %errorlevel%==0 (
del /f /q TkPicSplitter.spec
rd /s /q build
rd /s /q __pycache__
)

pause
exit


