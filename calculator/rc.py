"""
Módulo para cálculos de circuito RC.
τ = R × C
V(t) = V₀ × (1 - e^(-t/τ)) para carga
V(t) = V₀ × e^(-t/τ) para descarga
"""

import math


def calcular_constante_tempo(resistencia: float, capacitancia: float) -> float:
    """
    Calcula a constante de tempo τ (tau) de um circuito RC.
    
    Args:
        resistencia: Resistência em Ohms (Ω)
        capacitancia: Capacitância em Farads (F)
    
    Returns:
        Constante de tempo em segundos (s)
    
    Raises:
        ValueError: Se algum valor for negativo ou zero
    """
    if resistencia <= 0 or capacitancia <= 0:
        raise ValueError("Resistência e capacitância devem ser maiores que zero")
    
    return resistencia * capacitancia


def calcular_tensao_capacitor(v0: float, tau: float, tempo: float, 
                               carregando: bool = True) -> float:
    """
    Calcula a tensão no capacitor em um dado instante.
    
    Args:
        v0: Tensão inicial/final em Volts (V)
        tau: Constante de tempo em segundos (s)
        tempo: Tempo decorrido em segundos (s)
        carregando: True para carga, False para descarga
    
    Returns:
        Tensão no capacitor em Volts (V)
    
    Raises:
        ValueError: Se algum valor for negativo
    """
    if v0 < 0 or tau <= 0 or tempo < 0:
        raise ValueError("Valores devem ser positivos (tau > 0)")
    
    if carregando:
        return v0 * (1 - math.exp(-tempo / tau))
    else:
        return v0 * math.exp(-tempo / tau)


def calcular_rc(r: float, c: float, t: float, v0: float = 5.0, 
                carregando: bool = True) -> dict:
    """
    Calcula informações completas do circuito RC.
    
    Args:
        r: Resistência em Ohms (Ω)
        c: Capacitância em Farads (F)
        t: Tempo em segundos (s)
        v0: Tensão de referência em Volts (V)
        carregando: True para carga, False para descarga
    
    Returns:
        Dicionário com tau, tensão no tempo t, e percentual
    """
    tau = calcular_constante_tempo(r, c)
    v_t = calcular_tensao_capacitor(v0, tau, t, carregando)
    percentual = (v_t / v0) * 100 if v0 > 0 else 0
    
    return {
        'tau': tau,
        'tensao_t': v_t,
        'percentual': percentual,
        'tempo': t
    }
