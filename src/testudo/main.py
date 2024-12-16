import typer
import yaml
import logging
from rich.console import Console
from rich.logging import RichHandler

from .modules.attack_manager import AttackManager
from .modules.ai_advisor import AIAdvisor
from .utils.config_manager import ConfigManager

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler()]
)

console = Console()
app = typer.Typer()

@app.command()
def attack(
    target: str = typer.Argument(..., help="Cible à analyser"),
    mode: str = typer.Option("full", help="Mode : full, recon, network, web"),
    ai: bool = typer.Option(True, help="Utiliser l'IA pour l'analyse")
):
    """Lance une attaque automatisée selon la stratégie de la tortue romaine"""
    try:
        # Initialisation des composants
        config = ConfigManager.load_config()
        attack_manager = AttackManager(config)
        ai_advisor = AIAdvisor(config.get('gpt_api_key')) if ai else None

        # Affichage du début de l'attaque
        console.print(f"[bold blue]🛡️ Testudo - Démarrage de l'attaque sur {target}[/bold blue]")
        
        # Exécution des phases d'attaque
        phases = {
            'recon': 'Reconnaissance initiale',
            'fortification': 'Établissement de position',
            'scan': 'Analyse approfondie',
            'exploit': 'Tests d\'exploitation'
        }

        results = {}
        for phase_id, phase_name in phases.items():
            console.print(f"\n[bold yellow]Phase : {phase_name}[/bold yellow]")
            
            # Exécution de la phase
            phase_results = attack_manager.execute_phase(phase_id, target)
            results[phase_id] = phase_results
            
            # Analyse IA si activée
            if ai and ai_advisor:
                recommendations = ai_advisor.analyze_phase(phase_id, phase_results)
                console.print("\n[bold green]Recommandations IA :[/bold green]")
                for rec in recommendations:
                    console.print(f"▶️ {rec}")

        # Génération du rapport final
        report_path = attack_manager.generate_report(results)
        console.print(f"\n[bold green]✅ Rapport généré : {report_path}[/bold green]")

    except Exception as e:
        console.print(f"[bold red]❌ Erreur : {str(e)}[/bold red]")
        raise typer.Exit(1)

@app.command()
def setup(gpt_key: str = typer.Option(None, help="Clé API GPT")):
    """Configure l'outil avec les clés API nécessaires"""
    config = {}
    if gpt_key:
        config['gpt_api_key'] = gpt_key
        
    ConfigManager.save_config(config)
    console.print("[bold green]✅ Configuration sauvegardée[/bold green]")

if __name__ == "__main__":
    app()