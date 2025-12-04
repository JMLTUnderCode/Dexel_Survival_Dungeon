from dataclasses import dataclass, field
from typing import Dict

@dataclass
class TacticalProfile:
    """
    Descripción
        CLASE: Define los pesos (costos extra) para cada tipo de nodo táctico.
        Valor Positivo: Evitar nodo (Costo alto).
        Valor Negativo: Preferir nodo (Costo bajo/recompensa).

    Atributos
        - weights (Dict[str, float]): Diccionario mapeando 'tipo_tactico' -> peso.
    
    Métodos y Funciones
        - get_weight: Retorna el peso asociado a un tipo táctico.

    Propósito
        - Permitir que diferentes entidades valoren el terreno de forma distinta.
    """
    weights: Dict[str, float] = field(default_factory=dict)

    def get_weight(self, tactical_type: str) -> float:
        """
        Descripción
            MÉTODO: Obtiene el peso configurado para un tipo táctico.

        Argumentos
            - tactical_type (str) : El identificador del tipo (ej. 'cover', 'sentry').

        Retorno
            - float: El peso (positivo o negativo). 0.0 si no está definido.
        """
        return self.weights.get(tactical_type, 0.0)