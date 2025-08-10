@echo off
REM Create "pdf" folder if it doesn't exist
if not exist "pdf" mkdir "pdf"

REM Move all .pdf files (case-insensitive) to the "pdf" folder
move /Y *.pdf pdf\

echo Done! All PDF files moved to the "pdf" folder.
pause
