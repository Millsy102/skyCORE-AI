@echo off
:: 🔐 Protects the 'main' branch with required reviews and status checks

echo == Applying protection to 'main' branch ==

gh api --method PUT repos/Millsy102/skyCORE-AI/branches/main/protection ^
  --field required_status_checks='{"strict":true,"contexts":[]}' ^
  --field enforce_admins='{"enabled":true}' ^
  --field required_pull_request_reviews='{"dismiss_stale_reviews":true,"require_code_owner_reviews":false}' ^
  --field restrictions=null

echo ✅ Branch protection rules successfully applied.
pause
