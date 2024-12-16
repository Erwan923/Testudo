#!/usr/bin/env python3

import typer
import yaml
import logging
from rich.console import Console
from rich.logging import RichHandler
from pathlib import Path
from typing import Optional

from modules.attack_manager import AttackManager
from modules.ai_advisor import AIAdvisor
from modules.config_manager import ConfigManager

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler()]
)

console = Console()
app = typer.Typer()
config_manager = ConfigManager()

@app.command()
def setup(api_key: str):
    """Configure l'outil avec la clé API GPT"""
    config_manager.set_api_key(api_key)
    console.print("[green]Configuration sauvegardée avec succès ✓[/green]")

@app.command()
def attack(
    target: str,
    mode: str = typer.Option("full", help="Mode d'attaque: full, recon, network, web"),
    ai: bool = typer.Option(True, help="Utiliser l'IA pour l'analyse")
):
    """Lance une attaque automatisée sur la cible"""
    console.print(f"[bold blue]🛡️ Testudo - Démarrage de l'attaque sur {target}[/bold blue]")
    
    try:
        # Initialisation du gestionnaire d'attaque
        attack_manager = AttackManager(target)
        
        # Configuration de l'IA si activée
        if ai:
            api_key = config_manager.get_api_key()
            if not api_key:
                console.print("[yellow]⚠️ Pas de clé API configurée. L'analyse IA sera désactivée.[/yellow]")
                ai = False
            else:
                ai_advisor = AIAdvisor(api_key)
                attack_manager.set_ai_advisor(ai_advisor)

        # Exécution de l'attaque
        results = attack_manager.execute_attack(mode)
        
        # Affichage des résultats
        console.print("\n[bold green]📊 Résultats de l'attaque :[/bold green]")
        for phase, phase_results in results.items():
            console.print(f"\n[bold blue]{phase}[/bold blue]")
            console.print(phase_results)
            
            if ai:
                recommendations = ai_advisor.analyze_phase(phase, phase_results)
                console.print("\n[bold yellow]🤖 Recommandations IA :[/bold yellow]")
                console.print(recommendations)
                
        # Génération du rapport
        report_path = attack_manager.generate_report(results)
        console.print(f"\n[green]✓ Rapport généré : {report_path}[/green]")
        
    except Exception as e:
        console.print(f"[bold red]❌ Erreur : {str(e)}[/bold red]")
        raise typer.Exit(code=1)

@app.command()
def status():
    """Affiche le statut des pods et services"""
    try:
        from modules.kubernetes_manager import KubernetesManager
        k8s = KubernetesManager()
        status = k8s.get_status()
        
        console.print("[bold blue]📡 Statut des services :[/bold blue]")
        for service, service_status in status.items():
            icon = "✓" if service_status["healthy"] else "✗"
            color = "green" if service_status["healthy"] else "red"
            console.print(f"[{color}]{icon} {service}: {service_status['status']}[/{color}]")
    except Exception as e:
        console.print(f"[bold red]❌ Erreur : {str(e)}[/bold red]")

if __name__ == "__main__":
    app()