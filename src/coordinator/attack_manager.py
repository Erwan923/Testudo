from typing import Dict, List
import aiohttp
import asyncio
import logging
from enum import Enum

class AttackPhase(Enum):
    RECON = "recon"
    SCAN = "scan"
    EXPLOIT = "exploit"
    POST_EXPLOIT = "post_exploit"

class AttackManager:
    """Gestionnaire des attaques coordonnées"""
    
    def __init__(self):
        self.logger = logging.getLogger("Testudo.AttackManager")
        self.services = {
            AttackPhase.RECON: "http://testudo-osint:8081",
            AttackPhase.SCAN: "http://testudo-network:8082",
            AttackPhase.EXPLOIT: "http://testudo-exploit:8083",
        }
        
    async def execute_phase(self, phase: AttackPhase, target: str) -> Dict:
        """Exécute une phase d'attaque spécifique"""
        service_url = self.services.get(phase)
        if not service_url:
            raise ValueError(f"Service non trouvé pour la phase {phase}")
            
        try:
            async with aiohttp.ClientSession() as session:
                # Appelle le service approprié
                async with session.post(
                    f"{service_url}/execute",
                    json={"target": target}
                ) as response:
                    return await response.json()
                    
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de {phase}: {str(e)}")
            raise