@echo off
REM mCasei - Geracao diaria do triplet (13h Maputo)
setlocal
call "%~dp0set-env.bat"
cd /d "C:\Users\igorm\OneDrive\Documentos\Claude\Projects\mCaseiBot"
if not exist "automation\logs" mkdir "automation\logs"
set "STAMP=%date:~-4%-%date:~3,2%-%date:~0,2%"
echo ===== GERAR %STAMP% %time% ===== >> "automation\logs\gerar.log"
type "automation\runbook-gerar.md" | "C:\Users\igorm\AppData\Roaming\npm\claude.cmd" -p --permission-mode bypassPermissions --model sonnet >> "automation\logs\gerar.log" 2>&1
echo ===== FIM %time% ===== >> "automation\logs\gerar.log"
endlocal
