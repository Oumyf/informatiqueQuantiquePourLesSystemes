# 🔒 SSL Guides - Éliminer "Not Secure" sur Chrome 119+

## 📋 Vue d'ensemble

Collection de scripts et guides pour éliminer l'avertissement "Not secure" sur les certificats auto-signés, spécialement adapté pour **Chrome 119+** (post-2023) qui a supprimé le flag `allow-insecure-localhost`.

## 🎯 Problème résolu

- ❌ **Avant** : "Not secure" sur `https://localhost/smp/`
- ✅ **Après** : 🔒 "Connexion sécurisée" avec cadenas vert

## 🚀 Solutions disponibles

### 1. **Solution immédiate** (Temporaire)
```bash
# Lancer Chrome avec flags SSL
PowerShell -ExecutionPolicy Bypass -File "ssl-guides/launch_chrome_ssl.ps1"
```
**Résultat** : Chrome s'ouvre sans avertissement SSL

### 2. **Solution permanente** (Recommandée)
```bash
# Installer le certificat dans Windows
PowerShell -ExecutionPolicy Bypass -File "ssl-guides/install_cert_windows.ps1"
```
**Avantages** : Fonctionne avec tous les navigateurs

### 3. **Solution domaine local** (Alternative)
```bash
# Créer smp.local au lieu de localhost
PowerShell -ExecutionPolicy Bypass -File "ssl-guides/setup_local_domain.ps1"
```

## 📁 Structure des fichiers

```
ssl-guides/
├── chrome_modern_solutions.ps1     # Solutions Chrome 119+
├── launch_chrome_ssl.ps1           # Lancement Chrome avec flags
├── install_cert_windows.ps1        # Installation certificat Windows
├── setup_local_domain.ps1          # Configuration domaine local
├── configure_chrome_flags.ps1      # Configuration flags navigateur
├── guide_ssl_trust.ps1             # Guide général SSL
├── install_ssl_trust.ps1           # Installation certificat racine
├── guide_install_cert_manuel.ps1   # Guide installation manuelle
├── install_mkcert.ps1              # Installation outil mkcert
├── chrome_flags_simple.bat         # Flags Chrome (version simple)
├── guide_ssl_simple.bat           # Guide SSL simplifié
├── guide_multi_browsers.ps1        # Support multi-navigateurs
├── fix_apache_ssl.ps1              # Configuration Apache SSL
├── add_phpmyadmin.ps1              # Configuration phpMyAdmin
└── fix_apache_final.ps1            # Corrections Apache finales
```

## 🔧 Configuration Apache

Scripts pour configurer HTTPS sur XAMPP :
- `fix_apache_ssl.ps1` - Configuration SSL de base
- `add_phpmyadmin.ps1` - Ajout phpMyAdmin en HTTP
- `fix_apache_final.ps1` - Configuration finale

## 🌐 Support navigateurs

| Navigateur | Script spécialisé | Statut |
|------------|------------------|--------|
| Chrome 119+ | `launch_chrome_ssl.ps1` | ✅ Testé |
| Firefox | `configure_chrome_flags.ps1` | ✅ Supporté |
| Edge | `guide_multi_browsers.ps1` | ✅ Supporté |
| Opera | `guide_multi_browsers.ps1` | ✅ Supporté |

## 📖 Guides d'utilisation

### Pour Chrome moderne (119+)
1. Exécutez `chrome_modern_solutions.ps1` pour voir toutes les options
2. Choisissez entre solution temporaire ou permanente
3. Suivez les instructions à l'écran

### Pour installation permanente
1. Lancez `install_cert_windows.ps1`
2. Suivez le guide pas-à-pas
3. Redémarrez vos navigateurs
4. Testez sur `https://localhost/smp/`

## ⚡ Démarrage rapide

```bash
# 1. Clone ce repository
git clone <your-repo>

# 2. Solution immédiate
cd ssl-guides
PowerShell -ExecutionPolicy Bypass -File "launch_chrome_ssl.ps1"

# 3. Solution permanente (recommandée)
PowerShell -ExecutionPolicy Bypass -File "install_cert_windows.ps1"
```

## 🎯 Cas d'usage

- **Développement local** avec HTTPS
- **Démonstration** de projets sécurisés
- **Tests SSL** en environnement local
- **Applications RSA Post-Quantique**
- **Projets nécessitant HTTPS obligatoire**

## 📋 Prérequis

- Windows 10/11
- XAMPP avec Apache configuré
- Certificats SSL générés
- PowerShell (inclus dans Windows)

## 🔐 Sécurité

Ces scripts sont conçus pour l'**environnement de développement local uniquement**. Ne jamais utiliser en production avec des certificats auto-signés.

## 🤝 Contribution

- Scripts testés sur Windows 10/11
- Compatible Chrome 119+, Firefox, Edge
- Développé pour projets RSA Post-Quantique

## 📞 Support

Si vous rencontrez des problèmes :
1. Vérifiez que Apache/XAMPP fonctionne
2. Confirmez l'existence des certificats SSL
3. Exécutez en tant qu'administrateur si nécessaire
4. Consultez les guides détaillés dans chaque script

---

**Développé pour éliminer définitivement "Not secure" sur Chrome moderne ! 🚀**