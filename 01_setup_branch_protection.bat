@echo off
echo == Protecting 'main' branch from forced pushes ==
gh api -X PUT repos/Millsy102/skyCORE-AI/branches/main/protection ^
  -f required_status_checks='{"strict":true,"contexts":[]}' ^
  -f enforce_admins=true ^
  -f restrictions='null' ^
  -f required_pull_request_reviews='{"dismiss_stale_reviews":true}'
echo ✅ Branch protection set.
pause
