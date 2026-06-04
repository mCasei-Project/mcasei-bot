@echo off
REM mCasei - Verificacao de aprovacao (16h Maputo)
setlocal
call "%~dp0set-env.bat"
cd /d "C:\Users\igorm\OneDrive\Documentos\Claude\Projects\mCaseiBot"
if not exist "automation\logs" mkdir "automation\logs"
set "STAMP=%date:~-4%-%date:~3,2%-%date:~0,2%"
echo ===== APROVAR %STAMP% %time% ===== >> "automation\logs\aprovar.log"
type "automation\runbook-aprovar.md" | "C:\Users\igorm\AppData\Roaming\npm\claude.cmd" -p --permission-mode bypassPermissions --model sonnet >> "automation\logs\aprovar.log" 2>&1
echo ===== FIM %time% ===== >> "automation\logs\aprovar.log"
endlocal
