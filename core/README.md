# 🔐 Core RSA Post-Quantique

## Fichiers principaux

### `RSA_POST_QUANTIQUE.ipynb`
- **Description** : Implémentation 100% fait maison du système RSA Post-Quantique
- **Contenu** : 6 fonctions cryptographiques + 3 algorithmes mathématiques  
- **Validation** : ✅ Certifié fait maison (score 9/10)
- **Usage** : Ouvrir avec Jupyter Notebook

### `rsa_certificats_pq.py`
- **Description** : Module Python pour génération de certificats RSA PQ
- **Fonctions** : Génération clés, chiffrement, signature
- **Intégration** : Compatible avec l'application SMP

## 🧪 Tests
```bash
python ../demo-scripts/analyze_memoire_notebook.py
```

## 🔬 Validation
- Aucune bibliothèque cryptographique externe
- Utilise uniquement Python standard (math, random, time)
- Algorithmes implémentés manuellement
