# Guide pour éliminer "Not secure" avec certificat auto-signé
# Plusieurs méthodes disponibles selon les besoins

Write-Host "=== METHODES POUR ELIMINER 'NOT SECURE' ==="
Write-Host ""

Write-Host "1. METHODE NAVIGATEUR (Plus simple)"
Write-Host "   - Chrome: Cliquer sur 'Avance' puis 'Continuer vers localhost'"
Write-Host "   - Firefox: Cliquer sur 'Avance' puis 'Accepter le risque'"
Write-Host "   - Edge: Cliquer sur 'Avance' puis 'Continuer vers localhost'"
Write-Host ""

Write-Host "2. METHODE CERTIFICAT RACINE (Recommandee)"
Write-Host "   - Installer le certificat dans le magasin 'Autorites racines'"
Write-Host "   - Le navigateur fera confiance au certificat"
Write-Host ""

Write-Host "3. METHODE mkcert (Professionnelle)"
Write-Host "   - Outil pour generer des certificats locaux de confiance"
Write-Host "   - Automatiquement reconnus par tous les navigateurs"
Write-Host ""

Write-Host "4. METHODE FLAGS NAVIGATEUR (Developpement)"
Write-Host "   - Desactiver la verification SSL pour localhost"
Write-Host ""

Write-Host "Quelle methode voulez-vous utiliser ?"
Write-Host "Reponse recommandee: Methode 2 (Certificat racine)"