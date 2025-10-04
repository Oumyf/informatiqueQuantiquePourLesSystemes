# Script PowerShell pour corriger la configuration Apache
# Objectif: HTTPS pour SMP, HTTP normal pour XAMPP/phpmyadmin

$configFile = "C:\xampp\apache\conf\httpd.conf"
$content = Get-Content $configFile -Raw

# Supprimer les anciens VirtualHost problématiques
$content = $content -replace '(?s)# Virtual Host HTTP.*?</VirtualHost>', ''
$content = $content -replace '(?s)# Virtual Host HTTPS.*?</VirtualHost>', ''

# Ajouter la nouvelle configuration correcte
$newConfig = @"

# Virtual Host HTTPS pour SMP seulement
<VirtualHost *:443>
    DocumentRoot "C:/xampp/htdocs"
    ServerName localhost
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile "C:/xampp/apache/conf/ssl.crt/smp_rsa_pq.crt"
    SSLCertificateKeyFile "C:/xampp/apache/conf/ssl.key/smp_rsa_pq.key"
    SSLProtocol all -SSLv2 -SSLv3
    SSLCipherSuite HIGH:!aNULL:!MD5
    
    # Configuration globale pour htdocs
    <Directory "C:/xampp/htdocs">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
        DirectoryIndex index.php index.html
    </Directory>
    
    # Configuration spécifique pour SMP
    <Directory "C:/xampp/htdocs/smp">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
        DirectoryIndex index.php
    </Directory>
</VirtualHost>
"@

# Ajouter la nouvelle configuration
$content = $content + $newConfig

# Sauvegarder le fichier
$content | Set-Content $configFile -Encoding UTF8

Write-Host "Configuration Apache mise a jour"
Write-Host "Acces:"
Write-Host "   - HTTP XAMPP: http://localhost/phpmyadmin"  
Write-Host "   - HTTPS SMP:  https://localhost/smp/"
Write-Host "Redemarrez Apache pour appliquer"