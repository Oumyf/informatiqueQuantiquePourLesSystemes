# Methode 4 : Lancement Chrome avec flags SSL pour localhost
# Solution immediate pour Chrome 119+ sans installation

Write-Host "=== LANCEMENT CHROME AVEC FLAGS SSL ==="
Write-Host ""

# Fermer Chrome existant
Write-Host "1. Fermeture de Chrome existant..."
Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep 2

# Parametres Chrome pour ignorer les erreurs SSL localhost
$chromeFlags = @(
    "--ignore-certificate-errors-spki-list",
    "--ignore-ssl-errors",
    "--ignore-certificate-errors",
    "--allow-running-insecure-content",
    "--disable-web-security",
    "--user-data-dir=C:\temp\chrome-dev"
)

$chromeExe = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$chromeExe86 = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

# Detecter l'installation Chrome
$chromePath = $null
if (Test-Path $chromeExe) {
    $chromePath = $chromeExe
} elseif (Test-Path $chromeExe86) {
    $chromePath = $chromeExe86
} else {
    # Essayer via le PATH
    $chromePath = (Get-Command chrome -ErrorAction SilentlyContinue).Source
}

if ($chromePath) {
    Write-Host "2. Chrome trouve : $chromePath"
    Write-Host "3. Lancement avec flags SSL..."
    
    # Creer le repertoire temporaire
    $tempDir = "C:\temp\chrome-dev"
    if (-not (Test-Path $tempDir)) {
        New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
    }
    
    # Lancer Chrome avec les flags
    $arguments = $chromeFlags + @("https://localhost/smp/")
    Start-Process -FilePath $chromePath -ArgumentList $arguments
    
    Write-Host "4. Chrome lance avec flags SSL pour localhost"
    Write-Host "5. Votre SMP devrait s'ouvrir SANS avertissement 'Not secure'"
    
} else {
    Write-Host "Chrome non trouve. Alternatives :"
    Write-Host "- Methode 1 : Installation certificat Windows"
    Write-Host "- Methode 2 : mkcert"
}

Write-Host ""
Write-Host "NOTES :"
Write-Host "- Cette session Chrome ignore les erreurs SSL"
Write-Host "- Fermez cette fenetre pour revenir au Chrome normal"
Write-Host "- Pour usage permanent : installer le certificat (Methode 1)"