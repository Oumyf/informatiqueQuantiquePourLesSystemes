echo "=== GUIDE RAPIDE FLAGS CHROME ==="
echo.
echo "ETAPES SIMPLES :"
echo.
echo "1. Ouvrez Chrome"
echo "2. Tapez : chrome://flags/#allow-insecure-localhost"
echo "3. Trouvez : 'Allow invalid certificates for resources loaded from localhost'"
echo "4. Changez 'Default' vers 'Enabled'"
echo "5. Cliquez 'Relaunch' (redemarrer)"
echo "6. Testez : https://localhost/smp/"
echo.
echo "RESULTAT : Plus d'avertissement 'Not secure' !"
echo.
echo "AUTRES NAVIGATEURS :"
echo "- Edge : edge://flags/#allow-insecure-localhost"
echo "- Opera : opera://flags/#allow-insecure-localhost"
echo "- Firefox : about:config > security.tls.insecure_fallback_hosts = localhost"
echo.

rem Ouvrir Chrome sur les flags
start chrome "chrome://flags/#allow-insecure-localhost"