# Alternative: Installation et utilisation de mkcert
# Outil professionnel pour certificats SSL locaux de confiance

Write-Host "=== INSTALLATION MKCERT POUR SSL LOCAL ==="
Write-Host ""

# Vérifier si mkcert est déjà installé
$mkcertPath = Get-Command mkcert -ErrorAction SilentlyContinue

if ($mkcertPath) {
    Write-Host "mkcert deja installe: $($mkcertPath.Source)"
} else {
    Write-Host "1. Installation de mkcert via chocolatey..."
    
    # Vérifier si chocolatey est installé
    $choco = Get-Command choco -ErrorAction SilentlyContinue
    if (-not $choco) {
        Write-Host "   Installation de Chocolatey..."
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    }
    
    Write-Host "   Installation de mkcert..."
    choco install mkcert -y
}

Write-Host ""
Write-Host "2. Configuration mkcert pour localhost..."

# Créer l'autorité de certification locale
mkcert -install

# Générer un certificat pour localhost
$sslDir = "C:\xampp\apache\conf\ssl-mkcert"
if (-not (Test-Path $sslDir)) {
    New-Item -ItemType Directory -Path $sslDir -Force
}

Set-Location $sslDir
mkcert localhost 127.0.0.1 ::1

Write-Host ""
Write-Host "3. Certificats generes dans: $sslDir"
Write-Host "   - localhost+2.pem (certificat)"
Write-Host "   - localhost+2-key.pem (cle privee)"
Write-Host ""
Write-Host "4. Prochaine etape: Configurer Apache avec ces nouveaux certificats"

Set-Location "C:\xampp\htdocs\smp"