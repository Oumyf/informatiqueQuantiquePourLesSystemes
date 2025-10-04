# Methode 5 : Domaine local + Hosts (Alternative moderne)
# Creer smp.local au lieu de localhost pour eviter les restrictions Chrome

Write-Host "=== METHODE DOMAINE LOCAL (smp.local) ==="
Write-Host ""

# Modifier le fichier hosts
$hostsFile = "C:\Windows\System32\drivers\etc\hosts"
$hostsBackup = "C:\Windows\System32\drivers\etc\hosts.backup"
$domain = "smp.local"

Write-Host "1. Configuration du domaine local : $domain"
Write-Host ""

# Sauvegarder le fichier hosts
if (-not (Test-Path $hostsBackup)) {
    try {
        Copy-Item $hostsFile $hostsBackup -Force
        Write-Host "   ✅ Sauvegarde hosts creee"
    } catch {
        Write-Host "   ⚠️ Impossible de sauvegarder hosts (droits admin requis)"
    }
}

# Verifier si l'entree existe deja
$hostsContent = Get-Content $hostsFile -ErrorAction SilentlyContinue
if ($hostsContent -match $domain) {
    Write-Host "   ℹ️ Domaine $domain deja configure"
} else {
    Write-Host "2. Ajout dans le fichier hosts..."
    Write-Host "   Fichier : $hostsFile"
    Write-Host "   Entree a ajouter : 127.0.0.1    $domain"
    Write-Host ""
    Write-Host "   ATTENTION : Droits administrateur requis"
    Write-Host ""
    
    # Tentative d'ajout automatique
    try {
        $newEntry = "`n127.0.0.1    $domain"
        Add-Content -Path $hostsFile -Value $newEntry -Force
        Write-Host "   ✅ Domaine ajoute automatiquement"
    } catch {
        Write-Host "   ❌ Echec automatique. Ajout manuel requis :"
        Write-Host ""
        Write-Host "   METHODE MANUELLE :"
        Write-Host "   1. Ouvrez Notepad en tant qu'administrateur"
        Write-Host "   2. Ouvrez : $hostsFile"
        Write-Host "   3. Ajoutez a la fin : 127.0.0.1    $domain"
        Write-Host "   4. Sauvegardez"
    }
}

Write-Host ""
Write-Host "3. Configuration Apache pour $domain"
Write-Host "   Modifier httpd.conf :"
Write-Host "   - Ajouter ServerAlias $domain dans VirtualHost"
Write-Host "   - Ou creer un nouveau VirtualHost pour $domain"
Write-Host ""

Write-Host "4. Generer un nouveau certificat pour $domain"
Write-Host "   openssl req -x509 -newkey rsa:4096 -keyout smp_local.key -out smp_local.crt -days 365 -nodes -subj `/CN=$domain`"
Write-Host ""

Write-Host "5. Tester :"
Write-Host "   URL : https://$domain/smp/"
Write-Host "   Chrome acceptera plus facilement un domaine personnalise"
Write-Host ""

Write-Host "AVANTAGES :"
Write-Host "- Contourne les restrictions Chrome sur localhost"
Write-Host "- Plus professionnel"
Write-Host "- Simule un environnement de production"

# Ouvrir le fichier hosts pour edition manuelle
try {
    Start-Process "notepad.exe" -ArgumentList $hostsFile -Verb RunAs
    Write-Host ""
    Write-Host "6. ✅ Notepad ouvert en administrateur pour edition hosts"
} catch {
    Write-Host ""
    Write-Host "6. ⚠️ Ouvrez manuellement Notepad en admin pour editer hosts"
}