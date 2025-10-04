# Script pour installer le certificat SSL dans les autorités racines de confiance
# Cela éliminera définitivement l'avertissement "Not secure"

$certPath = "C:\xampp\apache\conf\ssl.crt\smp_rsa_pq.crt"

Write-Host "=== INSTALLATION CERTIFICAT SSL DANS AUTORITES RACINES ==="
Write-Host ""

# Vérifier que le certificat existe
if (-not (Test-Path $certPath)) {
    Write-Host "ERREUR: Certificat non trouve: $certPath"
    exit 1
}

Write-Host "1. Certificat trouve: $certPath"
Write-Host ""

# Méthode 1: Via PowerShell (automatique)
Write-Host "2. Installation automatique via PowerShell..."
try {
    # Importer le certificat dans le magasin racine de l'ordinateur local
    $cert = Import-Certificate -FilePath $certPath -CertStoreLocation "Cert:\LocalMachine\Root"
    Write-Host "   Certificat installe avec succes dans les autorites racines"
    Write-Host "   Empreinte: $($cert.Thumbprint)"
} catch {
    Write-Host "   Echec installation automatique: $($_.Exception.Message)"
    Write-Host ""
    Write-Host "3. Installation manuelle requise:"
    Write-Host "   - Clic droit sur: $certPath"
    Write-Host "   - Installer le certificat"
    Write-Host "   - Magasin: Ordinateur local"
    Write-Host "   - Emplacement: Autorites de certification racines de confiance"
}

Write-Host ""
Write-Host "4. Redemarrage des navigateurs requis"
Write-Host "5. Test: https://localhost/smp/"
Write-Host ""
Write-Host "RESULTAT ATTENDU: Cadenas vert, aucun avertissement"