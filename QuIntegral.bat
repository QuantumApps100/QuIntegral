pyinstaller --onefile --noconsole --name QuIntegral --icon="./QuIntegral-Icon.ico" QuIntegral.py
REM pyinstaller --onefile --name QuIntegral --icon="!/icons/QuIntegral-Icon.ico" QuIntegral.py
REM cd dist
REM del "../!/QuIntegral.exe"
REM ren "QuIntegral.exe" "../!/QuIntegral.exe"
REM del "../QuIntegral.spec"
REM Set-ItemProperty -Path "../!/QuIntegral.exe" -Name Publisher -Value "Quantum Apps"
REM cd ..