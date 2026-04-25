"""
Módulo calculator - Funções de cálculo para engenharia elétrica.
"""

from .ohm import calcular_ohm, calcular_tensao, calcular_corrente, calcular_resistencia
from .divider import calcular_divisor_tensao
from .rc import calcular_rc, calcular_constante_tempo, calcular_tensao_capacitor
from .color_code import decodificar_resistor_4_faixas, formatar_resistencia
from .power import calcular_potencia, verificar_limite_potencia

__all__ = [
    'calcular_ohm',
    'calcular_tensao',
    'calcular_corrente',
    'calcular_resistencia',
    'calcular_divisor_tensao',
    'calcular_rc',
    'calcular_constante_tempo',
    'calcular_tensao_capacitor',
    'decodificar_resistor_4_faixas',
    'formatar_resistencia',
    'calcular_potencia',
    'verificar_limite_potencia',
]
