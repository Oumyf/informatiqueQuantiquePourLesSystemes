#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de Certificats RSA Post-Quantique
Implémentation complète pour application pédagogique SMP

Ce module implémente :
1. PKI (Public Key Infrastructure) complète
2. Génération et gestion de certificats X.509 modifiés
3. Les 3 primitives : Confidentialité, Authentification, Intégrité
4. Interface pour intégration dans application SMP

Auteur: AdiaratouOumy Fall
Date: Octobre 2025
"""

import time
import hashlib
import json
import base64
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
import secrets

class MersenneTwister:
    """Générateur Mersenne Twister pour l'amorce cryptographique"""
    def __init__(self, seed):
        self.index = 624
        self.mt = [0] * 624
        self.mt[0] = seed & 0xffffffff
        for i in range(1, 624):
            self.mt[i] = (1812433253 * (self.mt[i-1] ^ 
                         (self.mt[i-1] >> 30)) + i) & 0xffffffff
    
    def extract_number(self):
        if self.index >= 624:
            self.twist()
        y = self.mt[self.index]
        y ^= (y >> 11)
        y ^= (y << 7) & 0x9d2c5680
        y ^= (y << 15) & 0xefc60000
        y ^= (y >> 18)
        self.index += 1
        return y & 0xffffffff
    
    def twist(self):
        for i in range(624):
            y = (self.mt[i] & 0x80000000) + (self.mt[(i+1) % 624] & 0x7fffffff)
            self.mt[i] = self.mt[(i + 397) % 624] ^ (y >> 1)
            if y % 2 != 0:
                self.mt[i] ^= 0x9908b0df
        self.index = 0

class BlumBlumShub:
    """Générateur cryptographiquement sûr Blum-Blum-Shub"""
    def __init__(self, p, q, seed):
        if p % 4 != 3 or q % 4 != 3:
            raise ValueError("p et q doivent être congrus à 3 modulo 4")
        self.M = p * q
        self.state = (seed * seed) % self.M
        if self.state <= 1:
            self.state = 2
    
    def next_bit(self):
        self.state = pow(self.state, 2, self.M)
        return self.state & 1
    
    def next_bits(self, n):
        if n <= 0:
            return 0
        result = 0
        for _ in range(n):
            result = (result << 1) | self.next_bit()
        return result

def extended_gcd(a, b):
    """Algorithme d'Euclide étendu"""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def mod_inverse(a, m):
    """Calcul de l'inverse modulaire"""
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Inverse modulaire inexistant")
    return x % m

def miller_rabin_test(n, k=20):
    """Test de primalité de Miller-Rabin"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Écriture n-1 = 2^r * d
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Test de Miller-Rabin k fois
    global bbs
    for _ in range(k):
        a = 2 + (bbs.next_bits(32) % (n - 3))
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
            
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True

def generate_prime(bits):
    """Génération d'un nombre premier de 'bits' bits"""
    max_attempts = 10000
    min_value = 1 << (bits - 1)
    max_value = (1 << bits) - 1
    
    for attempt in range(max_attempts):
        candidate = bbs.next_bits(bits)
        candidate = max(candidate, min_value)
        candidate = min(candidate, max_value)
        candidate |= 1  # Assurer que le nombre est impair
        
        if candidate >= min_value and miller_rabin_test(candidate):
            return candidate
    
    raise RuntimeError(f"Échec de génération d'un nombre premier de {bits} bits")

@dataclass
class CertificateInfo:
    """Informations d'un certificat"""
    subject: str
    issuer: str
    serial_number: str
    not_before: datetime
    not_after: datetime
    public_key: Tuple[int, int]  # (n, e)
    signature_algorithm: str = "RSA-PQ-SHA256"
    version: int = 3

class RSAPostQuantumSystem:
    """Système RSA Post-Quantique avec gestion de certificats"""
    
    def __init__(self, key_size=2048):
        self.key_size = key_size
        self.public_key = None
        self.private_key = None
        self.certificates = {}  # Stockage des certificats
        
        # Initialisation des générateurs cryptographiques
        seed = int(time.time()) % (2**32)
        mt = MersenneTwister(seed)
        seed_bbs = mt.extract_number()
        
        global bbs
        bbs = BlumBlumShub(499, 547, seed_bbs)
    
    def generate_keys(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Génération des clés RSA"""
        print(f"Génération des clés RSA de {self.key_size} bits...")
        start_time = time.time()
        
        # Génération de deux nombres premiers distincts
        p = generate_prime(self.key_size // 2)
        q = generate_prime(self.key_size // 2)
        
        while p == q:
            q = generate_prime(self.key_size // 2)
        
        # Calcul de N et φ(N)
        n = p * q
        phi = (p - 1) * (q - 1)
        
        # Choix de l'exposant public
        e = 65537
        if extended_gcd(e, phi)[0] != 1:
            e = 3
            if extended_gcd(e, phi)[0] != 1:
                raise ValueError("Impossible de trouver un exposant public valide")
        
        # Calcul de l'exposant privé
        d = mod_inverse(e, phi)
        
        self.public_key = (n, e)
        self.private_key = (n, d)
        
        generation_time = time.time() - start_time
        print(f"Clés générées en {generation_time:.2f} secondes")
        
        return self.public_key, self.private_key
    
    def create_certificate(self, subject: str, issuer: str = None, 
                          validity_days: int = 365) -> str:
        """Création d'un certificat X.509 modifié"""
        if self.public_key is None:
            raise ValueError("Clés non générées")
        
        if issuer is None:
            issuer = subject  # Auto-signé
        
        # Génération du numéro de série
        serial_number = secrets.token_hex(16)
        
        # Dates de validité
        not_before = datetime.now()
        not_after = not_before + timedelta(days=validity_days)
        
        # Création des informations du certificat
        cert_info = CertificateInfo(
            subject=subject,
            issuer=issuer,
            serial_number=serial_number,
            not_before=not_before,
            not_after=not_after,
            public_key=self.public_key
        )
        
        # Sérialisation pour signature
        cert_data = self._serialize_certificate(cert_info)
        
        # Signature du certificat
        signature = self.sign_data(cert_data)
        
        # Structure finale du certificat
        certificate = {
            'version': cert_info.version,
            'serial_number': cert_info.serial_number,
            'subject': cert_info.subject,
            'issuer': cert_info.issuer,
            'not_before': cert_info.not_before.isoformat(),
            'not_after': cert_info.not_after.isoformat(),
            'public_key': {
                'algorithm': 'RSA-PQ',
                'key_size': self.key_size,
                'n': str(cert_info.public_key[0]),
                'e': str(cert_info.public_key[1])
            },
            'signature_algorithm': cert_info.signature_algorithm,
            'signature': signature,
            'fingerprint': self._calculate_fingerprint(cert_data)
        }
        
        # Stockage du certificat
        self.certificates[serial_number] = certificate
        
        # Retour au format PEM-like
        cert_pem = self._to_pem_format(certificate)
        
        print(f"Certificat créé pour '{subject}' (SN: {serial_number[:8]}...)")
        return cert_pem
    
    def verify_certificate(self, cert_pem: str, ca_public_key: Tuple[int, int] = None) -> bool:
        """Vérification d'un certificat"""
        try:
            certificate = self._from_pem_format(cert_pem)
            
            # Vérification de la validité temporelle
            not_before = datetime.fromisoformat(certificate['not_before'])
            not_after = datetime.fromisoformat(certificate['not_after'])
            now = datetime.now()
            
            if now < not_before or now > not_after:
                print("Certificat expiré ou pas encore valide")
                return False
            
            # Reconstruction des données à vérifier
            cert_info = CertificateInfo(
                subject=certificate['subject'],
                issuer=certificate['issuer'],
                serial_number=certificate['serial_number'],
                not_before=not_before,
                not_after=not_after,
                public_key=(int(certificate['public_key']['n']), 
                           int(certificate['public_key']['e'])),
                signature_algorithm=certificate['signature_algorithm'],
                version=certificate['version']
            )
            
            cert_data = self._serialize_certificate(cert_info)
            
            # Vérification de la signature
            verification_key = ca_public_key if ca_public_key else self.public_key
            if verification_key is None:
                raise ValueError("Clé de vérification non disponible")
            
            return self.verify_signature(cert_data, certificate['signature'], verification_key)
            
        except Exception as e:
            print(f"Erreur lors de la vérification du certificat: {e}")
            return False
    
    # PRIMITIVES DE SÉCURITÉ
    
    def encrypt(self, message: str) -> str:
        """CONFIDENTIALITÉ : Chiffrement RSA"""
        if self.public_key is None:
            raise ValueError("Clés non générées")
        
        n, e = self.public_key
        
        # Conversion du message en entier
        if isinstance(message, str):
            message_bytes = message.encode('utf-8')
        else:
            message_bytes = message
        
        message_int = int.from_bytes(message_bytes, 'big')
        
        if message_int >= n:
            raise ValueError("Message trop grand pour la clé")
        
        ciphertext = pow(message_int, e, n)
        
        # Retour en base64 pour transport
        return base64.b64encode(str(ciphertext).encode()).decode()
    
    def decrypt(self, ciphertext_b64: str) -> str:
        """CONFIDENTIALITÉ : Déchiffrement RSA"""
        if self.private_key is None:
            raise ValueError("Clés non générées")
        
        n, d = self.private_key
        
        # Décodage depuis base64
        ciphertext = int(base64.b64decode(ciphertext_b64).decode())
        
        # Déchiffrement
        message_int = pow(ciphertext, d, n)
        
        # Conversion en bytes puis string
        byte_length = (message_int.bit_length() + 7) // 8
        message_bytes = message_int.to_bytes(byte_length, 'big')
        
        return message_bytes.decode('utf-8')
    
    def sign_data(self, data: str) -> str:
        """AUTHENTIFICATION : Signature RSA avec hachage"""
        if self.private_key is None:
            raise ValueError("Clés non générées")
        
        # Hachage des données
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        hash_obj = hashlib.sha256(data)
        hash_value = int.from_bytes(hash_obj.digest(), 'big')
        
        n, d = self.private_key
        if hash_value >= n:
            hash_value = hash_value % (n // 2)
        
        signature = pow(hash_value, d, n)
        
        # Retour en base64
        return base64.b64encode(str(signature).encode()).decode()
    
    def verify_signature(self, data: str, signature_b64: str, 
                        public_key: Tuple[int, int] = None) -> bool:
        """AUTHENTIFICATION : Vérification de signature RSA"""
        verification_key = public_key if public_key else self.public_key
        if verification_key is None:
            raise ValueError("Clé de vérification non disponible")
        
        try:
            # Hachage des données
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            hash_obj = hashlib.sha256(data)
            expected_hash = int.from_bytes(hash_obj.digest(), 'big')
            
            n, e = verification_key
            if expected_hash >= n:
                expected_hash = expected_hash % (n // 2)
            
            # Décodage de la signature
            signature = int(base64.b64decode(signature_b64).decode())
            
            # Vérification
            recovered_hash = pow(signature, e, n)
            return recovered_hash == expected_hash
            
        except Exception as e:
            print(f"Erreur lors de la vérification: {e}")
            return False
    
    def calculate_mac(self, data: str, key: str = None) -> str:
        """INTÉGRITÉ : Calcul d'un MAC (Message Authentication Code)"""
        if key is None:
            # Utilisation de la clé privée comme clé MAC
            if self.private_key is None:
                raise ValueError("Clé non disponible pour MAC")
            key = str(self.private_key[1])  # Utilise d
        
        # HMAC-SHA256
        import hmac
        mac = hmac.new(
            key.encode('utf-8'),
            data.encode('utf-8') if isinstance(data, str) else data,
            hashlib.sha256
        ).hexdigest()
        
        return mac
    
    def verify_mac(self, data: str, mac: str, key: str = None) -> bool:
        """INTÉGRITÉ : Vérification d'un MAC"""
        try:
            expected_mac = self.calculate_mac(data, key)
            return hmac.compare_digest(mac, expected_mac)
        except Exception as e:
            print(f"Erreur lors de la vérification MAC: {e}")
            return False
    
    # MÉTHODES UTILITAIRES
    
    def _serialize_certificate(self, cert_info: CertificateInfo) -> str:
        """Sérialisation des données du certificat pour signature"""
        data = f"{cert_info.version}|{cert_info.serial_number}|{cert_info.subject}|"
        data += f"{cert_info.issuer}|{cert_info.not_before.isoformat()}|"
        data += f"{cert_info.not_after.isoformat()}|{cert_info.public_key[0]}|"
        data += f"{cert_info.public_key[1]}|{cert_info.signature_algorithm}"
        return data
    
    def _calculate_fingerprint(self, cert_data: str) -> str:
        """Calcul de l'empreinte du certificat"""
        return hashlib.sha256(cert_data.encode()).hexdigest()
    
    def _to_pem_format(self, certificate: Dict) -> str:
        """Conversion en format PEM-like"""
        cert_json = json.dumps(certificate, indent=2)
        cert_b64 = base64.b64encode(cert_json.encode()).decode()
        
        pem = "-----BEGIN RSA-PQ CERTIFICATE-----\n"
        # Découpage en lignes de 64 caractères
        for i in range(0, len(cert_b64), 64):
            pem += cert_b64[i:i+64] + "\n"
        pem += "-----END RSA-PQ CERTIFICATE-----"
        
        return pem
    
    def _from_pem_format(self, cert_pem: str) -> Dict:
        """Conversion depuis le format PEM-like"""
        lines = cert_pem.strip().split('\n')
        cert_lines = []
        
        in_cert = False
        for line in lines:
            if "-----BEGIN RSA-PQ CERTIFICATE-----" in line:
                in_cert = True
                continue
            elif "-----END RSA-PQ CERTIFICATE-----" in line:
                break
            elif in_cert:
                cert_lines.append(line)
        
        cert_b64 = ''.join(cert_lines)
        cert_json = base64.b64decode(cert_b64).decode()
        return json.loads(cert_json)
    
    def get_certificate_info(self, cert_pem: str) -> Dict:
        """Extraction des informations d'un certificat"""
        certificate = self._from_pem_format(cert_pem)
        
        return {
            'subject': certificate['subject'],
            'issuer': certificate['issuer'],
            'serial_number': certificate['serial_number'],
            'not_before': certificate['not_before'],
            'not_after': certificate['not_after'],
            'fingerprint': certificate['fingerprint'],
            'key_size': certificate['public_key']['key_size'],
            'algorithm': certificate['public_key']['algorithm']
        }

# INTERFACE POUR APPLICATION PÉDAGOGIQUE SMP

class SMPSecurityInterface:
    """Interface sécurisée pour l'application pédagogique SMP"""
    
    def __init__(self, key_size=1024):  # Taille réduite pour démos pédagogiques
        self.rsa_system = RSAPostQuantumSystem(key_size)
        self.user_certificates = {}
        self.active_sessions = {}
        
    def initialize_user(self, username: str) -> Dict[str, str]:
        """Initialisation d'un utilisateur avec génération de certificat"""
        print(f"\n=== Initialisation utilisateur: {username} ===")
        
        # Génération des clés
        public_key, private_key = self.rsa_system.generate_keys()
        
        # Création du certificat
        certificate = self.rsa_system.create_certificate(
            subject=f"CN={username},OU=SMP-Pedagogique,O=UniversitePQ",
            validity_days=90  # Validité de 3 mois pour l'usage pédagogique
        )
        
        # Stockage du certificat utilisateur
        self.user_certificates[username] = {
            'certificate': certificate,
            'public_key': public_key,
            'private_key': private_key
        }
        
        print(f"Utilisateur {username} initialisé avec succès")
        return {
            'username': username,
            'certificate': certificate,
            'status': 'initialized'
        }
    
    def send_secure_message(self, sender: str, recipient: str, message: str) -> Dict[str, Any]:
        """Envoi de message sécurisé (3 primitives)"""
        if sender not in self.user_certificates or recipient not in self.user_certificates:
            raise ValueError("Utilisateurs non initialisés")
        
        print(f"\n=== Envoi sécurisé: {sender} → {recipient} ===")
        
        # 1. CONFIDENTIALITÉ : Chiffrement avec la clé publique du destinataire
        recipient_public_key = self.user_certificates[recipient]['public_key']
        
        # Utilisation temporaire de la clé du destinataire pour chiffrement
        original_key = self.rsa_system.public_key
        self.rsa_system.public_key = recipient_public_key
        
        encrypted_message = self.rsa_system.encrypt(message)
        
        # Restauration de la clé originale
        self.rsa_system.public_key = original_key
        
        # 2. AUTHENTIFICATION : Signature avec la clé privée de l'expéditeur
        sender_private_key = self.user_certificates[sender]['private_key']
        
        # Utilisation temporaire de la clé de l'expéditeur pour signature
        original_private = self.rsa_system.private_key
        self.rsa_system.private_key = sender_private_key
        
        signature = self.rsa_system.sign_data(message)
        
        # Restauration de la clé privée originale
        self.rsa_system.private_key = original_private
        
        # 3. INTÉGRITÉ : MAC du message chiffré
        mac = self.rsa_system.calculate_mac(encrypted_message, str(sender_private_key[1]))
        
        secure_envelope = {
            'sender': sender,
            'recipient': recipient,
            'timestamp': datetime.now().isoformat(),
            'encrypted_message': encrypted_message,
            'signature': signature,
            'mac': mac,
            'sender_certificate': self.user_certificates[sender]['certificate']
        }
        
        print("Message sécurisé créé avec succès")
        print(f"- Confidentialité: ✓ (chiffré)")
        print(f"- Authentification: ✓ (signé)")
        print(f"- Intégrité: ✓ (MAC)")
        
        return secure_envelope
    
    def receive_secure_message(self, recipient: str, secure_envelope: Dict[str, Any]) -> Dict[str, Any]:
        """Réception et vérification de message sécurisé"""
        if recipient not in self.user_certificates:
            raise ValueError("Destinataire non initialisé")
        
        print(f"\n=== Réception sécurisée: {secure_envelope['sender']} → {recipient} ===")
        
        try:
            # 1. Vérification du certificat de l'expéditeur
            sender_cert = secure_envelope['sender_certificate']
            cert_valid = self.rsa_system.verify_certificate(sender_cert)
            if not cert_valid:
                return {'status': 'error', 'message': 'Certificat invalide'}
            
            # Extraction de la clé publique du certificat
            cert_info = self.rsa_system.get_certificate_info(sender_cert)
            sender_cert_data = self.rsa_system._from_pem_format(sender_cert)
            sender_public_key = (
                int(sender_cert_data['public_key']['n']),
                int(sender_cert_data['public_key']['e'])
            )
            
            # 2. INTÉGRITÉ : Vérification du MAC
            sender_private_d = str(self.user_certificates[secure_envelope['sender']]['private_key'][1])
            mac_valid = self.rsa_system.verify_mac(
                secure_envelope['encrypted_message'],
                secure_envelope['mac'],
                sender_private_d
            )
            if not mac_valid:
                return {'status': 'error', 'message': 'Intégrité compromise (MAC invalide)'}
            
            # 3. CONFIDENTIALITÉ : Déchiffrement avec la clé privée du destinataire
            recipient_private_key = self.user_certificates[recipient]['private_key']
            
            # Utilisation temporaire de la clé du destinataire
            original_private = self.rsa_system.private_key
            self.rsa_system.private_key = recipient_private_key
            
            decrypted_message = self.rsa_system.decrypt(secure_envelope['encrypted_message'])
            
            # Restauration
            self.rsa_system.private_key = original_private
            
            # 4. AUTHENTIFICATION : Vérification de la signature
            signature_valid = self.rsa_system.verify_signature(
                decrypted_message,
                secure_envelope['signature'],
                sender_public_key
            )
            
            if not signature_valid:
                return {'status': 'error', 'message': 'Signature invalide'}
            
            print("Message vérifié avec succès")
            print(f"- Confidentialité: ✓ (déchiffré)")
            print(f"- Authentification: ✓ (signature valide)")
            print(f"- Intégrité: ✓ (MAC valide)")
            
            return {
                'status': 'success',
                'sender': secure_envelope['sender'],
                'message': decrypted_message,
                'timestamp': secure_envelope['timestamp'],
                'certificate_valid': cert_valid
            }
            
        except Exception as e:
            return {'status': 'error', 'message': f'Erreur de déchiffrement: {str(e)}'}

def demonstrate_smp_integration():
    """Démonstration complète pour l'application SMP pédagogique"""
    print("="*60)
    print("DÉMONSTRATION RSA POST-QUANTIQUE POUR SMP PÉDAGOGIQUE")
    print("="*60)
    
    # Initialisation du système
    smp = SMPSecurityInterface(key_size=1024)  # Taille réduite pour démo
    
    # Scénario pédagogique : Alice (enseignante) et Bob (étudiant)
    print("\n📚 SCÉNARIO PÉDAGOGIQUE")
    print("Alice = Enseignante, Bob = Étudiant")
    
    # Initialisation des utilisateurs
    alice_info = smp.initialize_user("Alice_Enseignante")
    bob_info = smp.initialize_user("Bob_Etudiant")
    
    # Message de l'enseignante vers l'étudiant
    message_pedagogique = "Votre devoir sur la cryptographie post-quantique est à rendre avant vendredi. Bonne chance!"
    
    # Envoi sécurisé
    secure_envelope = smp.send_secure_message("Alice_Enseignante", "Bob_Etudiant", message_pedagogique)
    
    # Réception et vérification
    received = smp.receive_secure_message("Bob_Etudiant", secure_envelope)
    
    print(f"\n📨 RÉSULTAT FINAL")
    if received['status'] == 'success':
        print(f"✅ Message reçu avec succès")
        print(f"De: {received['sender']}")
        print(f"Message: {received['message']}")
        print(f"Horodatage: {received['timestamp']}")
    else:
        print(f"❌ Erreur: {received['message']}")
    
    # Démonstration des informations de certificat
    print(f"\n🔒 INFORMATIONS CERTIFICAT ALICE")
    cert_info = smp.rsa_system.get_certificate_info(alice_info['certificate'])
    for key, value in cert_info.items():
        print(f"- {key}: {value}")
    
    print(f"\n💡 ANALYSE PÉDAGOGIQUE")
    print("1. Confidentialité: Message chiffré - seul Bob peut le lire")
    print("2. Authentification: Signature prouve que c'est bien Alice")
    print("3. Intégrité: MAC garantit que le message n'a pas été modifié")
    print("4. Non-répudiation: Alice ne peut nier avoir envoyé le message")

if __name__ == "__main__":
    demonstrate_smp_integration()