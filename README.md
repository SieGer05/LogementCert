# **LogementCert : Une Blockchain Transparente pour des Hébergements Certifiés à la Coupe du Monde 2030**
  
Une plateforme blockchain sécurisée et transparente pour la validation des logements, conçue pour prévenir la fraude locative et garantir des transactions immobilières fiables grâce au consensus Proof of Authority (PoA). Idéale pour gérer des annonces de logements vérifiées lors d'événements majeurs comme la **Coupe du Monde 2030 au Maroc** 🏆.

<p align="center">
     <a href="https://badge.fury.io/js/electron-markdownify">
          <img src="http://forthebadge.com/images/badges/built-with-love.svg">
          <img src="https://forthebadge.com/images/badges/open-source.png">
          <img src="https://forthebadge.com/images/badges/uses-git.png">
          <img src="https://forthebadge.com/images/badges/powered-by-coffee.png">
          <img src="https://forthebadge.com/images/badges/made-in-python.png">
     </a>
</p>

<p align="center">
  <a href="#aperçu-du-projet">Aperçu du projet</a> •
  <a href="#mise-en-œuvre-technique">Mise en œuvre technique</a> •
  <a href="#fonctionnalités-de-démonstration">Fonctionnalités de démonstration</a> •
  <a href="#statut-de-la-mise-en-œuvre-actuelle">Statut de la mise en œuvre actuelle</a> •
  <a href="#démarrage-rapide">Démarrage rapide</a> •
  <a href="#contribution">Contribution</a> •
  <a href="#licence">Licence</a>
</p>

## Aperçu du projet

### Contexte et objectifs

LogementCert est une plateforme basée sur la blockchain qui transforme les transactions immobilières en garantissant sécurité, transparence et confiance. Développée en prévision de la **Coupe du Monde 2030 au Maroc**, elle répond à la demande croissante de logements vérifiés tout en réduisant les risques de fraude locative. Grâce à un registre immuable et au consensus Proof of Authority (PoA), LogementCert offre un système fiable pour la validation et les transactions immobilières.

Nos objectifs principaux sont :

- **Prévenir la fraude** : Valider les annonces de logements de manière sécurisée pour protéger les utilisateurs.
    
- **Assurer la transparence** : Fournir un registre transparent pour tous les acteurs (propriétaires, locataires, autorités).
    
- **Simplifier les transactions** : Faciliter les transferts de propriété, les contrats de location et les enregistrements.
    

### Fonctionnalités clés

- **Registre immuable** : Historique des transactions inviolable.
    
- **Consensus flexible** : Supporte Proof-of-Authority (PoA) et Proof-of-Work (PoW).
    
- **Notarisation numérique** : Signatures RSA pour la validation des transactions.
    
- **Types de transactions** : Transferts de propriété, contrats de location, enregistrement de biens.
    
- **Interface conviviale** : Frontend responsive pour les propriétaires, autorités et locataires.

## Mise en œuvre technique


### Composants principaux

| Composant        | Fonctionnalités clés                                                   |
| ---------------- | ---------------------------------------------------------------------- |
| KeyManager       | Génération de clés RSA (2048 bits), empreintes, stockage sécurisé      |
| SignatureManager | Signature/verification numérique avec RSASSA-PSS                       |
| Block            | Structure blockchain personnalisée avec support PoA/PoW                |
| Blockchain       | Minage, validation, requêtes de transactions, persistance de la chaîne |
| Consensus        | Couche de consensus extensible (PoA implémenté)                        |
| Backend FastAPI  | API RESTful pour les interactions blockchain                           |
| Frontend         | Interface HTML/CSS/JS pour les utilisateurs et autorités               |

### Architecture

```
/logementCert
├── api/                     # API backend (FastAPI)
│   ├── routes/             # Routes API (auth, blockchain, listings)
│   ├── middleware/         # Middlewares (authentification, CORS, etc.)
│   ├── services/           # Logique métier (ex: gestion de la blockchain)
│   └── __init__.py
├── app/                     # Fichiers frontend (HTML/CSS/JS)
│   ├── css/                # Feuilles de style CSS
│   ├── js/                 # Scripts JavaScript pour l'interactivité
│   ├── index.html          # Page principale des annonces publiques
│   ├── login.html          # Page de connexion pour les utilisateurs
│   ├── authoritypanel.html # Tableau de bord pour les autorités
│   └── ownerdashboard.html # Tableau de bord pour les propriétaires
├── blockchain/             # Logique de la blockchain
│   ├── block.py            # Définition de la structure d'un bloc
│   ├── blockchain.py       # Classe principale de la blockchain
│   └── consensus.py        # Mécanismes de consensus (PoA, PoW, etc.)
├── crypto/                 # Fonctions cryptographiques
│   ├── key_manager.py      # Gestion des clés RSA (génération, stockage)
│   ├── signature.py        # Signature et vérification des données
│   └── __init__.py
├── .gitignore              # Fichier pour ignorer les fichiers/dossiers dans Git
├── example_usage.py        # Exemple de script pour utiliser les composants
├── README.md               # Documentation et instructions du projet
├── main.py                 # Point d'entrée principal de l'application
```

## Fonctionnalités de démonstration

LogementCert propose les fonctionnalités suivantes, entièrement opérationnelles :

- **Minage PoW** : Simuler le minage des transactions immobilières.
    
- **Validation PoA** : Autoriser les transactions avec des validateurs de confiance.
    
- **Persistance de la chaîne** : Sauvegarder et charger l'état de la blockchain via JSON.
    
- **Recherche de transactions** : Récupérer les transactions par adresse ou statut.
    
- **Interface utilisateur** :
    
    - Page des annonces publiques pour parcourir les propriétés validées.
        
    - Tableau de bord des propriétaires pour soumettre des biens.
        
    - Panneau des autorités pour valider les transactions.
        
    - Système de réservation pour les locataires.
        


## Statut de la mise en œuvre actuelle

Le projet **LogementCert est entièrement terminé**, avec toutes les fonctionnalités principales implémentées, testées et documentées. Le système est prêt pour un déploiement ou une personnalisation selon les besoins des utilisateurs.

### Fonctionnalités terminées

#### Blockchain principale

- Système de consensus hybride (PoW/PoA switchable).
    
- Initialisation du bloc de genèse.
    
- Flux de validation des blocs.
    

#### Cryptographie

- Gestion du cycle de vie des clés RSA.
    
- Signatures numériques avec protection contre les relectures.
    
- Empreintes des clés (SHA-256 tronqué).
    

#### Gestion des données

- Système de file d'attente pour les transactions.
    
- Persistance de la chaîne en JSON.
    
- Requêtes de transactions par adresse.
    

#### API et Frontend

- API RESTful avec FastAPI pour les interactions blockchain.
    
- Frontend responsive pour les utilisateurs publics, propriétaires et autorités.
    
- Système de connexion sécurisé.
    

#### Tests et validation

- Suite de tests complète pour les opérations blockchain.
    
- Tests manuels des endpoints API et des flux frontend.

## Démarrage rapide

### Prérequis

Assurez-vous d'avoir installé les éléments suivants :

- **Python 3.9+** : Pour exécuter l'API backend.
    
- **pip** : Gestionnaire de paquets Python.
    
- Un navigateur web moderne (Chrome, Firefox, etc.) pour le frontend.
    

### Installation

1. **Cloner le dépôt** :
    
    ```bash
    hhttps://github.com/SieGer05/LogementCert.git
    cd LogementCert
    ```
    
2. **Configurer un environnement virtuel** (optionnel mais recommandé) :
    
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows : venv\Scripts\activate
    ```
    
3. **Installer les dépendances** :
    
    ```bash
    pip install -r requirements.txt
    ```
    
    Aucune dépendance supplémentaire n'est requise pour le frontend.

### Exécution du projet

1. **Lancer l'API backend** :
    
    ```bash
    python main.py
    ```
    
    L'API sera accessible à http://localhost:8000.
    
2. **Servir le frontend** :
    
    - Utilisez un serveur HTTP simple :
        
        ```bash
        cd app
        python -m http.server 8080
        ```
        
    - Ouvre http://localhost:8080 dans votre navigateur.
        
3. **Accéder à l'application** :
    
    - Commencez par index.html pour parcourir les annonces publiques.
        
    - Connectez-vous via login.html (ex. : username=admin, password=admin, role=authority pour un accès autorité).
        
### Exemples d'utilisation

- **Utilisateur public** :
    
    - Parcourir les annonces sur index.html.
        
    - Réserver un bien via le formulaire de réservation.
        
- **Propriétaire** :
    
    - Se connecter avec username=owner, password=owner, role=owner.
        
    - Soumettre un bien via ownerdashboard.html.
        
- **Autorité** :
    
    - Se connecter avec username=admin, password=admin, role=authority.
        
    - Valider les transactions via authoritypanel.html.

## Contribution

LogementCert est maintenant terminé, mais nous accueillons les contributions pour la maintenance ou les améliorations ! Pour contribuer :

1. Faites un fork du dépôt.
    
2. Créez une nouvelle branche (git checkout -b fonctionnalité/votre-fonctionnalité).
    
3. Apportez vos modifications et validez-les (git commit -m "Ajouter votre fonctionnalité").
    
4. Poussez vers votre fork (git push origin fonctionnalité/votre-fonctionnalité).
    
5. Ouvrez une pull request avec une description détaillée de vos changements.
    

Veuillez respecter les guidelines de style du projet et inclure des tests si vous ajoutez de nouvelles fonctionnalités.

## Les contributeurs:

<a href="https://github.com/othneildrew/Best-README-Template/graphs/contributors">
  <img src="https://avatars.githubusercontent.com/u/112343397?v=4" width="50" height="50" style="border-radius: 50%; margin-right: 5px;" />
  <img src="https://avatars.githubusercontent.com/u/80603216?v=4" width="50" height="50" style="border-radius: 50%; margin-right: 5px;" />
  <img src="https://avatars.githubusercontent.com/u/92984861?v=4" width="50" height="50" style="border-radius: 50%; margin-right: 5px;" />
</a>

## Licence

Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus de détails.
