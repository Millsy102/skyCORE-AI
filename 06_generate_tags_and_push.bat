@echo off
echo == Tagging current commit as v1.0 and pushing tag ==
git tag v1.0
git push origin v1.0
echo ✅ Tag created and pushed.
pause