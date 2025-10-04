# Methode 1 : Installation certificat dans Windows (Solution permanente)
# Fonctionne pour Chrome 119+, Edge, Firefox, tous navigateurs

Write-Host "=== INSTALLATION CERTIFICAT WINDOWS (PERMANENTE) ==="
Write-Host ""

$certPath = "C:\xampp\apache\conf\ssl.crt\smp_rsa_pq.crt"

if (-not (Test-Path $certPath)) {
    Write-Host "Erreur : Certificat non trouve : $certPath"
    exit 1
}

Write-Host "1. Certificat trouve : $certPath"
Write-Host "2. Installation dans le magasin Windows..."

# Methode via certlm.msc (plus fiable)
Write-Host ""
Write-Host "METHODE MANUELLE (RECOMMANDEE) :"
Write-Host ""
Write-Host "A. Via l'interface Windows :"
Write-Host "   1. Appuyez Win+R"
Write-Host "   2. Tapez : certlm.msc"
Write-Host "   3. Allez dans : Autorites de certification racines de confiance > Certificats"
Write-Host "   4. Clic droit > Toutes les taches > Importer"
Write-Host "   5. Selectionnez : $certPath"
Write-Host "   6. Terminez l'importation"
Write-Host ""

Write-Host "B. Via l'Explorateur (SIMPLE) :"
Write-Host "   1. Double-clic sur : $certPath"
Write-Host "   2. Cliquez : 'Installer le certificat'"
Write-Host "   3. Emplacement : 'Ordinateur local'"
Write-Host "   4. Magasin : 'Autorites de certification racines de confiance'"
Write-Host "   5. Validez l'installation"
Write-Host ""

Write-Host "3. Apres installation :"
Write-Host "   - Redemarrez TOUS les navigateurs"
Write-Host "   - Testez : https://localhost/smp/"
Write-Host "   - Resultat : Cadenas vert, 'Connexion securisee'"
Write-Host ""

# Ouvrir le gestionnaire de certificats et l'explorateur
Write-Host "4. Ouverture automatique des outils..."

try {
    # Ouvrir le gestionnaire de certificats
    Start-Process "certlm.msc"
    Write-Host "   ✅ Gestionnaire de certificats ouvert"
} catch {
    Write-Host "   ⚠️ Gestionnaire de certificats non accessible"
}

try {
    # Ouvrir l'explorateur sur le certificat
    Start-Process "explorer.exe" -ArgumentList "/select,`"$certPath`""
    Write-Host "   ✅ Explorateur ouvert sur le certificat"
} catch {
    Write-Host "   ⚠️ Impossible d'ouvrir l'explorateur"
}

Write-Host ""
Write-Host "AVANTAGES DE CETTE METHODE :"
Write-Host "- Fonctionne avec Chrome 119+"
Write-Host "- Compatible tous navigateurs"
Write-Host "- Solution permanente"
Write-Host "- Professionnel et securise"