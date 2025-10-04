# Script pour copier tous les guides SSL vers le repository GitHub
# Organisation des solutions pour eliminer "Not secure" sur Chrome 119+

Write-Host "=== COPIE DES GUIDES SSL VERS GITHUB REPO ==="
Write-Host ""

$sourceDir = "C:\xampp\htdocs\smp"
$targetDir = "C:\xampp\htdocs\github-repo\ssl-guides"

# Creer le dossier ssl-guides dans le repo
if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    Write-Host "✅ Dossier ssl-guides cree"
}

# Liste des fichiers SSL a copier
$sslFiles = @(
    "guide_ssl_trust.ps1",
    "install_ssl_trust.ps1", 
    "install_mkcert.ps1",
    "guide_install_cert_manuel.ps1",
    "guide_ssl_simple.bat",
    "fix_apache_ssl.ps1",
    "add_phpmyadmin.ps1",
    "fix_apache_final.ps1",
    "fix_listen_443.ps1",
    "fix_documentroot.ps1",
    "chrome_modern_solutions.ps1",
    "launch_chrome_ssl.ps1",
    "install_cert_windows.ps1",
    "setup_local_domain.ps1",
    "configure_chrome_flags.ps1",
    "guide_multi_browsers.ps1",
    "chrome_flags_simple.bat"
)

$copiedCount = 0

Write-Host "Copie des fichiers SSL :"
foreach ($file in $sslFiles) {
    $sourcePath = Join-Path $sourceDir $file
    $targetPath = Join-Path $targetDir $file
    
    if (Test-Path $sourcePath) {
        try {
            Copy-Item $sourcePath $targetPath -Force
            Write-Host "  ✅ $file"
            $copiedCount++
        } catch {
            Write-Host "  ❌ Echec: $file"
        }
    } else {
        Write-Host "  ⚠️  Non trouve: $file"
    }
}

Write-Host ""
Write-Host "📊 RESUME :"
Write-Host "  - Fichiers copies: $copiedCount"
Write-Host "  - Destination: $targetDir"
Write-Host ""
Write-Host "Guides SSL prets pour GitHub !"