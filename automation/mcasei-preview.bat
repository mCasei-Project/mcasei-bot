@echo off
REM mCasei - PREVIEW (gera + email, sem Buffer) para validacao
setlocal
call "%~dp0set-env.bat"
cd /d "C:\Users\igorm\OneDrive\Documentos\Claude\Projects\mCaseiBot"
if not exist "automation\logs" mkdir "automation\logs"
echo ===== PREVIEW %date% %time% ===== >> "automation\logs\preview.log"
type "automation\runbook-preview.md" | "C:\Users\igorm\AppData\Roaming\npm\claude.cmd" -p --permission-mode bypassPermissions --model sonnet >> "automation\logs\preview.log" 2>&1
echo ===== FIM %time% ===== >> "automation\logs\preview.log"
endlocal
