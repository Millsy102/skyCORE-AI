@echo off
echo skyCORE-AI Installer
echo ---------------------
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ✅ Done! Launching skyCORE-AI...
python ui/main_window.py

echo.
echo Need help? Join the Discord: https://discord.gg/m4ZCy2UbCY
pause