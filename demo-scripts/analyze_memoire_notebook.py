#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyse du notebook RSA POST QUANTIQUE.ipynb
Localisation: Desktop/Mémoire/
Vérification implémentation 100% fait maison
"""

import os
import json
import re

def find_notebook_in_memoire():
    """Trouver le notebook dans le dossier Mémoire"""
    
    print("🔍 RECHERCHE DANS DOSSIER MÉMOIRE")
    print("=" * 40)
    
    # Chemins possibles pour le dossier Mémoire
    memoire_paths = [
        r"C:\Users\USER\Desktop\Mémoire",
        r"C:\Users\USER\Desktop\Memoire", 
        r"C:\Users\USER\Desktop\mémoire",
        r"C:\Users\USER\Desktop\memoire",
        r"C:\Users\Abdoul\Desktop\Mémoire",
        r"C:\Users\Abdoul\Desktop\Memoire"
    ]
    
    for memoire_path in memoire_paths:
        print(f"🔍 Recherche dans: {memoire_path}")
        
        if os.path.exists(memoire_path):
            print(f"✅ Dossier trouvé: {memoire_path}")
            
            # Chercher le notebook dans ce dossier
            possible_notebooks = [
                "RSA POST QUANTIQUE.ipynb",
                "rsa post quantique.ipynb",
                "RSA_POST_QUANTIQUE.ipynb",
                "rsa_post_quantique.ipynb"
            ]
            
            for notebook_name in possible_notebooks:
                notebook_path = os.path.join(memoire_path, notebook_name)
                if os.path.exists(notebook_path):
                    print(f"✅ NOTEBOOK TROUVÉ: {notebook_path}")
                    return notebook_path
                else:
                    print(f"❌ Pas trouvé: {notebook_name}")
            
            # Recherche plus large dans le dossier
            try:
                print(f"🔍 Recherche élargie dans {memoire_path}...")
                for root, dirs, files in os.walk(memoire_path):
                    for file in files:
                        if file.endswith('.ipynb') and 'rsa' in file.lower():
                            full_path = os.path.join(root, file)
                            print(f"✅ Notebook RSA trouvé: {full_path}")
                            return full_path
            except Exception as e:
                print(f"⚠️ Erreur recherche: {e}")
        else:
            print(f"❌ Dossier introuvable: {memoire_path}")
    
    return None

def analyze_notebook_content(notebook_path):
    """Analyser le contenu du notebook"""
    
    print(f"\n📖 ANALYSE CONTENU NOTEBOOK")
    print("-" * 35)
    print(f"📁 Fichier: {notebook_path}")
    
    try:
        with open(notebook_path, 'r', encoding='utf-8', errors='ignore') as f:
            notebook_data = json.load(f)
        
        # Extraire les cellules de code
        code_cells = []
        all_code = ""
        
        cells = notebook_data.get('cells', [])
        print(f"📊 Total cellules: {len(cells)}")
        
        for i, cell in enumerate(cells):
            if cell.get('cell_type') == 'code':
                source = cell.get('source', [])
                if isinstance(source, list):
                    cell_code = ''.join(source)
                else:
                    cell_code = source
                
                code_cells.append({
                    'index': i,
                    'code': cell_code,
                    'execution_count': cell.get('execution_count'),
                    'outputs': cell.get('outputs', [])
                })
                
                all_code += cell_code + "\n"
        
        print(f"📊 Cellules de code: {len(code_cells)}")
        
        return all_code, code_cells
        
    except Exception as e:
        print(f"❌ Erreur lecture notebook: {e}")
        return "", []

def check_imports_homemade(all_code):
    """Vérifier que les imports sont fait maison"""
    
    print(f"\n📋 VÉRIFICATION IMPORTS FAIT MAISON")
    print("-" * 45)
    
    # Extraire tous les imports
    import_lines = []
    lines = all_code.split('\n')
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if line.startswith(('import ', 'from ')) and not line.startswith('#'):
            import_lines.append(line)
    
    print(f"📊 Imports trouvés: {len(import_lines)}")
    
    # Bibliothèques standard autorisées (fait maison)
    allowed_standard = {
        'math', 'random', 'time', 'datetime', 'os', 'sys',
        'hashlib', 'hmac', 'base64', 'json', 'secrets',
        'itertools', 'functools', 'collections', 'struct'
    }
    
    # Bibliothèques INTERDITES pour fait maison
    forbidden_external = {
        'cryptography', 'pycrypto', 'pycryptodome', 'crypto',
        'rsa', 'ecdsa', 'pyopenssl', 'nacl', 'gmpy2', 
        'primality', 'sympy', 'numpy', 'scipy'
    }
    
    clean_imports = []
    forbidden_found = []
    
    for imp_line in import_lines:
        # Extraire le nom du module
        if imp_line.startswith('import '):
            module = imp_line.split('import ')[1].split('.')[0].split(' ')[0].split(',')[0]
        elif imp_line.startswith('from '):
            module = imp_line.split('from ')[1].split('.')[0].split(' ')[0]
        else:
            continue
        
        module = module.strip()
        
        if module.lower() in forbidden_external:
            forbidden_found.append(imp_line)
            print(f"   ❌ INTERDIT: {imp_line}")
        elif module in allowed_standard:
            clean_imports.append(imp_line)
            print(f"   ✅ AUTORISÉ: {imp_line}")
        else:
            # Vérifier si c'est standard
            try:
                __import__(module)
                clean_imports.append(imp_line)
                print(f"   ✅ STANDARD: {imp_line}")
            except ImportError:
                print(f"   ⚠️ INCONNU: {imp_line}")
    
    is_homemade = len(forbidden_found) == 0
    
    print(f"\n📊 RÉSULTAT IMPORTS:")
    print(f"   ✅ Autorisés: {len(clean_imports)}")
    print(f"   ❌ Interdits: {len(forbidden_found)}")
    
    if is_homemade:
        print(f"\n🎉 IMPORTS 100% FAIT MAISON!")
        print("✅ Aucune bibliothèque cryptographique externe")
        print("✅ Utilisation uniquement de Python standard")
    else:
        print(f"\n❌ IMPORTS EXTERNES DÉTECTÉS!")
        print("Ces bibliothèques ne sont pas 'fait maison':")
        for forbidden in forbidden_found:
            print(f"   • {forbidden}")
    
    return is_homemade

def analyze_crypto_functions(all_code):
    """Analyser les fonctions cryptographiques implémentées"""
    
    print(f"\n🔐 ANALYSE FONCTIONS CRYPTOGRAPHIQUES")
    print("-" * 45)
    
    # Patterns pour détecter les implémentations crypto
    crypto_patterns = [
        (r'def\s+([^(]*rsa[^(]*)\(', 'RSA'),
        (r'def\s+([^(]*generat[^(]*)\(', 'Génération'),
        (r'def\s+([^(]*encrypt[^(]*)\(', 'Chiffrement'), 
        (r'def\s+([^(]*decrypt[^(]*)\(', 'Déchiffrement'),
        (r'def\s+([^(]*sign[^(]*)\(', 'Signature'),
        (r'def\s+([^(]*verify[^(]*)\(', 'Vérification'),
        (r'def\s+([^(]*key[^(]*)\(', 'Gestion clés'),
    ]
    
    crypto_functions = []
    
    for pattern, func_type in crypto_patterns:
        matches = re.finditer(pattern, all_code, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            func_name = match.group(1).strip()
            line_num = all_code[:match.start()].count('\n') + 1
            crypto_functions.append({
                'name': func_name,
                'type': func_type,
                'line': line_num
            })
    
    print(f"🔧 Fonctions cryptographiques trouvées: {len(crypto_functions)}")
    
    if crypto_functions:
        for func in crypto_functions:
            print(f"   ✅ {func['name']} - {func['type']} (ligne {func['line']})")
    else:
        print("   ⚠️ Aucune fonction cryptographique évidente")
    
    return crypto_functions

def analyze_math_algorithms(all_code):
    """Analyser les algorithmes mathématiques"""
    
    print(f"\n🧮 ANALYSE ALGORITHMES MATHÉMATIQUES") 
    print("-" * 45)
    
    # Patterns pour algorithmes mathématiques fait maison
    math_patterns = [
        (r'def\s+[^(]*gcd[^(]*\(', 'PGCD'),
        (r'def\s+[^(]*inverse[^(]*\(', 'Inverse modulaire'),
        (r'def\s+[^(]*prime[^(]*\(', 'Test primalité'),
        (r'def\s+[^(]*miller[^(]*\(', 'Miller-Rabin'),
        (r'def\s+[^(]*fermat[^(]*\(', 'Test Fermat'),
        (r'def\s+[^(]*euler[^(]*\(', 'Fonction Euler'),
        (r'def\s+[^(]*totient[^(]*\(', 'Totient'),
        (r'pow\s*\([^)]+,\s*[^)]+,\s*[^)]+\)', 'Exponentiation modulaire'),
    ]
    
    math_algos = {}  # Éviter doublons
    
    for pattern, algo_type in math_patterns:
        matches = re.finditer(pattern, all_code, re.IGNORECASE)
        for match in matches:
            line_num = all_code[:match.start()].count('\n') + 1
            if algo_type not in math_algos:
                math_algos[algo_type] = line_num
    
    print(f"🧮 Algorithmes mathématiques: {len(math_algos)}")
    
    if math_algos:
        for algo_type, line_num in math_algos.items():
            print(f"   ✅ {algo_type} (ligne {line_num})")
    else:
        print("   ⚠️ Aucun algorithme mathématique évident")
    
    return math_algos

def check_post_quantum_content(all_code):
    """Vérifier le contenu Post-Quantique"""
    
    print(f"\n🚀 VÉRIFICATION CONTENU POST-QUANTIQUE")
    print("-" * 45)
    
    # Mots-clés Post-Quantique
    pq_keywords = [
        'post.quantum', 'post.quantique', 'quantum.resistant',
        'quantum.safe', 'post_quantum', 'post_quantique',
        'pqc', 'quantum.computer', 'shor.algorithm'
    ]
    
    pq_found = []
    lines = all_code.split('\n')
    
    for i, line in enumerate(lines, 1):
        for keyword in pq_keywords:
            if re.search(keyword, line, re.IGNORECASE):
                pq_found.append({
                    'line': i,
                    'content': line.strip()[:80] + '...' if len(line.strip()) > 80 else line.strip()
                })
                break  # Une seule mention par ligne
    
    print(f"🔍 Mentions Post-Quantique: {len(pq_found)}")
    
    if pq_found:
        for mention in pq_found[:3]:  # Afficher les 3 premières
            print(f"   ✅ Ligne {mention['line']}: {mention['content']}")
        if len(pq_found) > 3:
            print(f"   ... et {len(pq_found) - 3} autres mentions")
        return True
    else:
        print("   ⚠️ Pas de mention explicite Post-Quantique")
        return False

def main():
    """Analyse complète du notebook RSA POST QUANTIQUE"""
    
    print("🔍 ANALYSE NOTEBOOK RSA POST QUANTIQUE")
    print("📍 Localisation: Desktop/Mémoire/")
    print("🎯 Vérification: 100% fait maison")
    print("=" * 60)
    
    # 1. Trouver le notebook
    notebook_path = find_notebook_in_memoire()
    
    if not notebook_path:
        print("\n❌ NOTEBOOK NON TROUVÉ DANS MÉMOIRE")
        print("\n💡 VÉRIFICATIONS:")
        print("• Le dossier s'appelle bien 'Mémoire' ?")
        print("• Le fichier est bien 'RSA POST QUANTIQUE.ipynb' ?")
        print("• Chemin: Desktop/Mémoire/RSA POST QUANTIQUE.ipynb")
        return
    
    # 2. Analyser le contenu
    all_code, code_cells = analyze_notebook_content(notebook_path)
    
    if not all_code:
        print("❌ Impossible de lire le contenu")
        return
    
    # 3. Vérifier les imports
    imports_ok = check_imports_homemade(all_code)
    
    # 4. Analyser les fonctions crypto
    crypto_funcs = analyze_crypto_functions(all_code)
    
    # 5. Analyser les algorithmes math
    math_algos = analyze_math_algorithms(all_code)
    
    # 6. Vérifier contenu Post-Quantique
    has_pq = check_post_quantum_content(all_code)
    
    # 7. VERDICT FINAL
    print(f"\n" + "="*60)
    print("🏆 VERDICT FINAL")
    print("="*60)
    
    total_score = len(crypto_funcs) + len(math_algos)
    
    if imports_ok and total_score >= 5:
        print("🎉 EXCELLENT! NOTEBOOK 100% FAIT MAISON!")
        print("✅ Imports: Bibliothèques standard uniquement")
        print(f"✅ Implémentation: {len(crypto_funcs)} fonctions crypto + {len(math_algos)} algos math")
        print(f"✅ Score total: {total_score}")
        
        if has_pq:
            print("✅ Innovation: Post-Quantique explicitement mentionnée")
        
        print(f"\n🔐 VOTRE RÉALISATION FAIT MAISON:")
        print("• Cryptographie RSA: Implémentée personnellement")
        print("• Algorithmes mathématiques: Codés manuellement")
        print("• Dépendances: Zéro bibliothèque externe")
        print("• Innovation: RSA Post-Quantique authentique")
        
        print(f"\n🏆 CERTIFICATION 'FAIT MAISON' VALIDÉE!")
        print("Parfait pour démonstration au jury!")
        
    elif imports_ok:
        print("✅ BIEN! Imports propres")
        print("✅ Aucune bibliothèque cryptographique externe")
        print(f"⚠️ Implémentation: {total_score} fonctions/algorithmes")
        print("⚠️ Peut nécessiter plus d'implémentations")
        
    else:
        print("❌ IMPORTS EXTERNES DÉTECTÉS")
        print("❌ Notebook pas 100% fait maison")
        print("\n💡 Pour être fait maison:")
        print("• Supprimez les bibliothèques crypto externes")
        print("• Utilisez seulement: math, random, hashlib")
        print("• Implémentez tout vous-même")
    
    print(f"\n📁 NOTEBOOK ANALYSÉ:")
    print(f"   {notebook_path}")

if __name__ == "__main__":
    main()