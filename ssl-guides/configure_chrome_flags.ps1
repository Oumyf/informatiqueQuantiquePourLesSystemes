# Guide pour configurer les flags Chrome pour SSL localhost
# Eliminer definitivement "Not secure" avec les flags navigateur

Write-Host "=== CONFIGURATION FLAGS CHROME POUR SSL LOCALHOST ==="
Write-Host ""

Write-Host "FLAGS CHROME A ACTIVER :"
Write-Host ""

Write-Host "1. FLAG PRINCIPAL (Le plus important) :"
Write-Host "   URL: chrome://flags/#allow-insecure-localhost"
Write-Host "   Nom: 'Allow invalid certificates for resources loaded from localhost'"
Write-Host "   Action: ACTIVER (Enable)"
Write-Host ""

Write-Host "2. FLAG COMPLEMENTAIRE :"
Write-Host "   URL: chrome://flags/#ignore-certificate-errors-spki-list"
Write-Host "   Nom: 'Ignore certificate errors on these origins'"
Write-Host "   Action: ACTIVER (Enable)"
Write-Host ""

Write-Host "3. FLAG WEBTRANSPORT (Que vous avez trouve) :"
Write-Host "   URL: chrome://flags/#webtransport-developer-mode"
Write-Host "   Nom: 'WebTransport Developer Mode'"
Write-Host "   Action: ACTIVER (Enable) - Optionnel"
Write-Host ""

Write-Host "PROCEDURE :"
Write-Host ""
Write-Host "1. Ouvrez Chrome"
Write-Host "2. Tapez dans la barre d'adresse : chrome://flags/"
Write-Host "3. Recherchez : 'allow-insecure-localhost'"
Write-Host "4. Changez de 'Default' vers 'Enabled'"
Write-Host "5. Cliquez 'Relaunch' pour redemarrer Chrome"
Write-Host "6. Testez : https://localhost/smp/"
Write-Host ""

Write-Host "ALTERNATIVE FIREFOX :"
Write-Host ""
Write-Host "1. Tapez : about:config"
Write-Host "2. Recherchez : security.tls.insecure_fallback_hosts"
Write-Host "3. Ajoutez : localhost"
Write-Host "4. Redemarrez Firefox"
Write-Host ""

Write-Host "RESULTAT ATTENDU :"
Write-Host "- Plus d'avertissement 'Not secure'"
Write-Host "- Cadenas vert ou gris (securise)"
Write-Host "- Acces direct a https://localhost/smp/"

# Ouvrir automatiquement Chrome sur la page des flags
Write-Host ""
Write-Host "Ouverture automatique de Chrome sur les flags..."
Start-Process "chrome.exe" -ArgumentList "chrome://flags/#allow-insecure-localhost"