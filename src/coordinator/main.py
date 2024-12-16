import os
import sys
import yaml
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List, Optional
from enum import Enum

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('Testudo.Coordinator')

app = FastAPI(title="Testudo Coordinator")

class AttackPhase(str, Enum):
    RECONNAISSANCE = "recon"
    SCAN = "scan"
    EXPLOIT = "exploit"
    POST_EXPLOIT = "post_exploit"

class AttackRequest(BaseModel):
    target: str
    phase: AttackPhase
    options: Optional[Dict] = None

class PhaseResult(BaseModel):
    phase: str
    status: str
    findings: List[Dict]
    recommendations: Optional[List[str]] = None

@app.post("/attack", response_model=PhaseResult)
async def start_attack(request: AttackRequest):
    """Lance une phase d'attaque spécifique"""
    logger.info(f"Démarrage de la phase {request.phase} sur {request.target}")
    
    try:
        # Vérifie que la cible est valide
        if not validate_target(request.target):
            raise ValueError("Cible invalide")
            
        # Charge la configuration de la phase
        phase_config = load_phase_config(request.phase)
        
        # Exécute la phase appropriée
        if request.phase == AttackPhase.RECONNAISSANCE:
            result = await execute_recon_phase(request.target, phase_config)
        elif request.phase == AttackPhase.SCAN:
            result = await execute_scan_phase(request.target, phase_config)
        elif request.phase == AttackPhase.EXPLOIT:
            result = await execute_exploit_phase(request.target, phase_config)
        else:
            result = await execute_post_exploit_phase(request.target, phase_config)
            
        # Analyse les résultats avec l'IA si configurée
        if os.getenv("GPT_API_KEY"):
            recommendations = await analyze_with_ai(result)
            result["recommendations"] = recommendations
            
        return PhaseResult(**result)
        
    except Exception as e:
        logger.error(f"Erreur lors de l'attaque: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    """Récupère le statut de tous les composants"""
    try:
        from kubernetes import client, config
        
        # Charge la configuration k8s
        config.load_incluster_config()
        v1 = client.CoreV1Api()
        
        # Vérifie le statut des pods
        pods = v1.list_namespaced_pod(namespace="default", label_selector="app=testudo")
        status = {}
        
        for pod in pods.items:
            status[pod.metadata.name] = {
                "status": pod.status.phase,
                "ready": all(cont.ready for cont in pod.status.container_statuses)
            }
            
        return status
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du statut: {str(e)}")
        return {"error": str(e)}

def validate_target(target: str) -> bool:
    """Valide que la cible est autorisée"""
    # Implémentez votre logique de validation ici
    return True

def load_phase_config(phase: AttackPhase) -> Dict:
    """Charge la configuration pour une phase spécifique"""
    try:
        with open("/app/config/phases.yaml", "r") as f:
            config = yaml.safe_load(f)
        return config.get(phase, {})
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la configuration: {str(e)}")
        return {}

async def execute_recon_phase(target: str, config: Dict) -> Dict:
    """Exécute la phase de reconnaissance"""
    # Implémentez la logique de reconnaissance ici
    pass

async def execute_scan_phase(target: str, config: Dict) -> Dict:
    """Exécute la phase de scan"""
    # Implémentez la logique de scan ici
    pass

async def execute_exploit_phase(target: str, config: Dict) -> Dict:
    """Exécute la phase d'exploitation"""
    # Implémentez la logique d'exploitation ici
    pass

async def execute_post_exploit_phase(target: str, config: Dict) -> Dict:
    """Exécute la phase de post-exploitation"""
    # Implémentez la logique de post-exploitation ici
    pass

async def analyze_with_ai(result: Dict) -> List[str]:
    """Analyse les résultats avec l'IA"""
    try:
        import openai
        openai.api_key = os.getenv("GPT_API_KEY")
        
        # Formatage du prompt pour l'IA
        prompt = f"""En tant qu'expert en sécurité, analyse ces résultats:
        Phase: {result['phase']}
        Résultats: {result['findings']}
        
        Quelles sont les prochaines étapes recommandées?"""
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en sécurité offensive."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content.split('\n')
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse IA: {str(e)}")
        return []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)