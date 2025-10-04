# GUIDE COMPLET: Eliminer "Not secure" - Methode manuelle simple
# Installation du certificat SSL dans les autorites racines de Windows

Write-Host "=== GUIDE MANUEL POUR ELIMINER 'NOT SECURE' ==="
Write-Host ""

$certFile = "C:\xampp\apache\conf\ssl.crt\smp_rsa_pq.crt"

Write-Host "ETAPES A SUIVRE:"
Write-Host ""

Write-Host "1. 📁 OUVRIR L'EXPLORATEUR DE FICHIERS"
Write-Host "   Naviguez vers: $certFile"
Write-Host ""

Write-Host "2. 🖱️  CLIC DROIT sur le fichier smp_rsa_pq.crt"
Write-Host "   Selectionnez: 'Installer le certificat'"
Write-Host ""

Write-Host "3. 🏪 ASSISTANT D'IMPORTATION"
Write-Host "   - Emplacement du magasin: 'Ordinateur local' (IMPORTANT)"
Write-Host "   - Cliquez: 'Suivant'"
Write-Host ""

Write-Host "4. 📍 EMPLACEMENT DU CERTIFICAT"
Write-Host "   - Selectionnez: 'Placer tous les certificats dans le magasin suivant'"
Write-Host "   - Cliquez: 'Parcourir'"
Write-Host "   - Choisissez: 'Autorites de certification racines de confiance'"
Write-Host "   - Cliquez: 'OK' puis 'Suivant'"
Write-Host ""

Write-Host "5. ⚠️  AVERTISSEMENT DE SECURITE"
Write-Host "   - Message: 'Voulez-vous installer ce certificat?'"
Write-Host "   - Repondez: 'OUI' (c'est notre certificat SMP)"
Write-Host ""

Write-Host "6. ✅ CONFIRMATION"
Write-Host "   - Message: 'L'importation a reussi'"
Write-Host "   - Cliquez: 'OK'"
Write-Host ""

Write-Host "7. 🔄 REDEMARRER LES NAVIGATEURS"
Write-Host "   - Fermez completement Chrome/Firefox/Edge"
Write-Host "   - Rouvrez et testez: https://localhost/smp/"
Write-Host ""

Write-Host "RESULTAT ATTENDU: 🔒 Cadenas vert, 'Connexion securisee'"
Write-Host ""

# Ouvrir automatiquement l'explorateur sur le certificat
Write-Host "8. 🚀 OUVERTURE AUTOMATIQUE DE L'EXPLORATEUR..."
Start-Process "explorer.exe" -ArgumentList "/select,`"$certFile`""

Write-Host ""
Write-Host "Le fichier certificat est maintenant selectionne dans l'explorateur."
Write-Host "Suivez les etapes ci-dessus pour l'installer."