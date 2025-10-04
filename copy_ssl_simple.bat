echo "=== COPIE DES GUIDES SSL VERS GITHUB ==="
echo.

rem Creer le dossier ssl-guides
if not exist "ssl-guides" mkdir "ssl-guides"

rem Copier les fichiers SSL depuis SMP
copy "C:\xampp\htdocs\smp\*ssl*.ps1" "ssl-guides\" >nul 2>&1
copy "C:\xampp\htdocs\smp\*ssl*.bat" "ssl-guides\" >nul 2>&1
copy "C:\xampp\htdocs\smp\*chrome*.ps1" "ssl-guides\" >nul 2>&1
copy "C:\xampp\htdocs\smp\*chrome*.bat" "ssl-guides\" >nul 2>&1
copy "C:\xampp\htdocs\smp\*apache*.ps1" "ssl-guides\" >nul 2>&1
copy "C:\xampp\htdocs\smp\*cert*.ps1" "ssl-guides\" >nul 2>&1
copy "C:\xampp\htdocs\smp\*domain*.ps1" "ssl-guides\" >nul 2>&1
copy "C:\xampp\htdocs\smp\*phpmyadmin*.ps1" "ssl-guides\" >nul 2>&1

echo "Fichiers SSL copies dans ssl-guides/"
echo.

rem Compter les fichiers
for /f %%i in ('dir /b ssl-guides\*.* ^| find /c /v ""') do set count=%%i
echo "Nombre de fichiers: %count%"

echo.
echo "Guides SSL prets pour GitHub !"

rem Lister les fichiers copies
echo.
echo "Fichiers copies:"
dir /b ssl-guides\