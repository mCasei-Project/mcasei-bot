@echo off
REM mCasei - Geracao diaria do triplet (13h Maputo)
setlocal
call "%~dp0set-env.bat"
cd /d "C:\Users\igorm\OneDrive\Documentos\Claude\Projects\mCaseiBot"
if not exist "automation\logs" mkdir "automation\logs"
REM Data de hoje em ISO (YYYY-MM-DD), robusta e independente do locale: fonte unica da verdade
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set "DATA=%%i"
echo ===== GERAR %DATA% %time% ===== >> "automation\logs\gerar.log"
( echo INSTRUCAO CRITICA: A DATA DE HOJE E %DATA%. Usa EXATAMENTE esta data ^(formato YYYY-MM-DD^) como DATA em toda a pipeline: pasta Posts\DATA, meta.data, assunto do email e --date. NAO recalcules nem adivinhes a data.& echo.& type "automation\runbook-gerar.md" ) | "C:\Users\igorm\AppData\Roaming\npm\claude.cmd" -p --permission-mode bypassPermissions --model sonnet >> "automation\logs\gerar.log" 2>&1
echo ===== FIM %time% ===== >> "automation\logs\gerar.log"
endlocal
