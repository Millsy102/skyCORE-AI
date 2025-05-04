@echo off
:: 🌍 Sets 'main' as default and makes repo public

@echo off
echo == Setting default branch to 'main' and making public ==
gh repo edit --default-branch main --visibility public
echo ✅ Repo is now public and main is default.
pause
