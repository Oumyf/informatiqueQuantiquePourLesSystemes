# Script pour corriger Apache - HTTPS seulement pour SMP
# HTTP normal pour phpMyAdmin et XAMPP

$configFile = "C:\xampp\apache\conf\httpd.conf"
$content = Get-Content $configFile -Raw

# Supprimer l'ancien VirtualHost HTTPS global
$content = $content -replace '(?s)# Virtual Host HTTPS.*?</VirtualHost>', ''

# Ajouter la configuration corrigée
$newConfig = @"

# Configuration HTTPS seulement pour SMP via RewriteRule
# Pas de VirtualHost global HTTPS pour préserver phpMyAdmin en HTTP

# SSL Configuration pour les connexions HTTPS
<IfModule mod_ssl.c>
    Listen 443 ssl
    SSLEngine on
    SSLCertificateFile "C:/xampp/apache/conf/ssl.crt/smp_rsa_pq.crt"
    SSLCertificateKeyFile "C:/xampp/apache/conf/ssl.key/smp_rsa_pq.key"
    SSLProtocol all -SSLv2 -SSLv3
    SSLCipherSuite HIGH:!aNULL:!MD5
</IfModule>
"@

$content = $content + $newConfig
$content | Set-Content $configFile -Encoding UTF8

Write-Host "Configuration Apache corrigee:"
Write-Host "- HTTP: localhost/phpmyadmin (normal)"
Write-Host "- HTTPS: localhost/smp (securise)"