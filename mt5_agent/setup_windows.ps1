# Installe Python, Git, MT5 et l'agent sur un VPS Windows (à lancer dans PowerShell en administrateur)
$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$tmp = "$env:TEMP\mt5setup"; New-Item -ItemType Directory -Force $tmp | Out-Null

Write-Host "1/4 Python..."
Invoke-WebRequest "https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe" -OutFile "$tmp\python.exe"
Start-Process "$tmp\python.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait

Write-Host "2/4 Git..."
Invoke-WebRequest "https://github.com/git-for-windows/git/releases/download/v2.47.0.windows.1/Git-2.47.0-64-bit.exe" -OutFile "$tmp\git.exe"
Start-Process "$tmp\git.exe" -ArgumentList "/VERYSILENT /NORESTART" -Wait
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine")

Write-Host "3/4 MetaTrader 5..."
Invoke-WebRequest "https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe" -OutFile "$tmp\mt5.exe"
Start-Process "$tmp\mt5.exe" -ArgumentList "/auto" -Wait

Write-Host "4/4 Agent..."
Set-Location $HOME
if (-not (Test-Path sam)) { git clone -b claude/quirky-einstein-o3amcd https://github.com/idehmani/sam }
python -m pip install --upgrade pip
python -m pip install MetaTrader5 pandas requests
Write-Host "Terminé. Ouvrez MT5, connectez votre compte, éditez $HOME\sam\mt5_agent\config.py puis lancez : python $HOME\sam\mt5_agent\agent.py"
