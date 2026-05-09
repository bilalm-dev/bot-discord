# ServerMate — Bot Discord

Un bot Discord polyvalent avec des commandes utilitaires, des mini-jeux et de la gestion de serveur. Projet réalisé en autonomie pour démontrer mes compétences en développement Python et consommation d'APIs externes.

## Stack technique

- **Python 3.12** + **discord.py** — framework bot Discord
- **OpenWeatherMap API** — données météo en temps réel
- **asyncio** — gestion asynchrone des tâches

## Fonctionnalités

- `/meteo [ville]` — météo en temps réel via API externe
- `/info` — statistiques du serveur Discord
- `/aide` — liste des commandes disponibles
- `/quiz` — quiz interactif avec boutons et timer 30s
- `/rappel [secondes] [message]` — rappel différé avec mention

## Lancer le projet en local

### Prérequis
- Python 3.12+
- Un compte Discord Developer
- Une clé API OpenWeatherMap

### Installation

```bash
# Cloner le repo
git clone https://github.com/bilalmdev164/discord-bot.git
cd discord-bot

# Créer et activer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
# Remplis les variables dans .env
```

### Lancer le bot

```bash
python3 main.py
```

## Structure du projet

```
discord-bot/
├── cogs/
│   ├── utilitaires.py   # /meteo, /info, /aide
│   └── jeux.py          # /quiz, /rappel
├── main.py              # Point d'entrée du bot
├── .env.example         # Template des variables d'environnement
└── requirements.txt
```

## Ce que j'ai appris

- Créer un bot Discord avec des commandes slash modernes
- Consommer une API externe en temps réel
- Utiliser la programmation asynchrone avec asyncio
- Créer des interfaces interactives avec des boutons Discord
- Organiser un projet Python en modules (Cogs)