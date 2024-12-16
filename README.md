# Testudo 🛡️

## À propos
Testudo est un outil d'audit de sécurité automatisé qui utilise la stratégie de la tortue romaine : une progression méthodique et sécurisée.

## Fonctionnement
1. Lecture des cheatsheets (fiches techniques en markdown)
2. Analyse sécurisée de la cible
3. Génération et exécution de playbooks Ansible
4. Consolidation des positions acquises

## Installation
```bash
git clone https://github.com/Erwan923/Testudo.git
cd Testudo
pip install -r requirements.txt
```

## Utilisation
```bash
python3 testudo.py --target [IP] --mode [recon|scan|exploit]
```

## Structure
- `testudo.py` : Script principal
- `cheatsheets/` : Fiches techniques markdown
- `playbooks/` : Playbooks Ansible générés
- `reports/` : Rapports d'analyse