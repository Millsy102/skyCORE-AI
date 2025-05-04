@echo off
echo == Enabling Issues, Discussions, and Wiki ==
gh repo edit --add-readme --has-issues=true --has-wiki=true --has-projects=true
gh api -X PATCH repos/Millsy102/skyCORE-AI -f has_discussions=true
echo ✅ Collaboration features enabled.
pause
