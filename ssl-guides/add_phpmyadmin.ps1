# Script pour ajouter phpMyAdmin à Apache
# Ajouter l'alias pour accéder à phpMyAdmin via /phpmyadmin

$configFile = "C:\xampp\apache\conf\httpd.conf"
$content = Get-Content $configFile -Raw

# Configuration phpMyAdmin à ajouter
$phpMyAdminConfig = @"

# Configuration phpMyAdmin
Alias /phpmyadmin "C:/xampp/phpMyAdmin/"
Alias /phpMyAdmin "C:/xampp/phpMyAdmin/"

<Directory "C:/xampp/phpMyAdmin">
    AllowOverride AuthConfig
    Require all granted
    DirectoryIndex index.php
</Directory>
"@

# Ajouter la configuration avant la fin du fichier
$content = $content + $phpMyAdminConfig

# Sauvegarder
$content | Set-Content $configFile -Encoding UTF8

Write-Host "phpMyAdmin configure :"
Write-Host "- Acces via: http://localhost/phpmyadmin/"
Write-Host "- Repertoire: C:\xampp\phpMyAdmin\"