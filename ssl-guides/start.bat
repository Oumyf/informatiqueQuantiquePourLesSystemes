echo "=== SSL GUIDES - DEMARRAGE RAPIDE ==="
echo.
echo "Solutions pour eliminer 'Not secure' sur Chrome 119+"
echo.
echo "CHOISISSEZ VOTRE SOLUTION :"
echo.
echo "1. SOLUTION IMMEDIATE (Temporaire)"
echo "   - Lance Chrome avec flags SSL"
echo "   - Fonctionne immediatement"
echo "   - Commande: PowerShell -File launch_chrome_ssl.ps1"
echo.
echo "2. SOLUTION PERMANENTE (Recommandee)"
echo "   - Installe certificat dans Windows"
echo "   - Fonctionne avec tous navigateurs"
echo "   - Commande: PowerShell -File install_cert_windows.ps1"
echo.
echo "3. SOLUTION DOMAINE LOCAL (Alternative)"
echo "   - Cree smp.local au lieu de localhost"
echo "   - Contourne restrictions Chrome"
echo "   - Commande: PowerShell -File setup_local_domain.ps1"
echo.
echo "4. GUIDE COMPLET"
echo "   - Toutes les options disponibles"
echo "   - Commande: PowerShell -File chrome_modern_solutions.ps1"
echo.

set /p choice="Entrez votre choix (1-4): "

if "%choice%"=="1" (
    echo.
    echo "Lancement solution immediate..."
    PowerShell -ExecutionPolicy Bypass -File "launch_chrome_ssl.ps1"
) else if "%choice%"=="2" (
    echo.
    echo "Lancement solution permanente..."
    PowerShell -ExecutionPolicy Bypass -File "install_cert_windows.ps1"
) else if "%choice%"=="3" (
    echo.
    echo "Lancement solution domaine local..."
    PowerShell -ExecutionPolicy Bypass -File "setup_local_domain.ps1"
) else if "%choice%"=="4" (
    echo.
    echo "Affichage guide complet..."
    PowerShell -ExecutionPolicy Bypass -File "chrome_modern_solutions.ps1"
) else (
    echo.
    echo "Choix invalide. Relancez le script."
)

echo.
echo "Consultez README.md pour plus d'informations"
pause