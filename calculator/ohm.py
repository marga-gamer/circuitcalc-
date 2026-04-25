"""
Módulo para cálculos da Lei de Ohm.
V = I × R
"""

from typing import Optional


def calcular_tensao(corrente: float, resistencia: float) -> float:
    """
    Calcula a tensão usando V = I × R.
    
    Args:
        corrente: Corrente em Amperes (A)
        resistencia: Resistência em Ohms (Ω)
    
    Returns:
        Tensão em Volts (V)
    
    Raises:
        ValueError: Se algum valor for negativo
    """
    if corrente < 0 or resistencia < 0:
        raise ValueError("Corrente e resistência devem ser valores positivos")
    return corrente * resistencia


def calcular_corrente(tensao: float, resistencia: float) -> float:
    """
    Calcula a corrente usando I = V / R.
    
    Args:
        tensao: Tensão em Volts (V)
        resistencia: Resistência em Ohms (Ω)
    
    Returns:
        Corrente em Amperes (A)
    
    Raises:
        ValueError: Se algum valor for negativo ou resistência for zero
    """
    if tensao < 0 or resistencia < 0:
        raise ValueError("Tensão e resistência devem ser valores positivos")
    if resistencia == 0:
        raise ValueError("Resistência não pode ser zero")
    return tensao / resistencia


def calcular_resistencia(tensao: float, corrente: float) -> float:
    """
    Calcula a resistência usando R = V / I.
    
    Args:
        tensao: Tensão em Volts (V)
        corrente: Corrente em Amperes (A)
    
    Returns:
        Resistência em Ohms (Ω)
    
    Raises:
        ValueError: Se algum valor for negativo ou corrente for zero
    """
    if tensao < 0 or corrente < 0:
        raise ValueError("Tensão e corrente devem ser valores positivos")
    if corrente == 0:
        raise ValueError("Corrente não pode ser zero")
    return tensao / corrente


def calcular_ohm(v: Optional[float] = None, 
                 i: Optional[float] = None, 
                 r: Optional[float] = None) -> dict:
    """
    Calcula a grandeza faltante na Lei de Ohm dados dois valores.
    
    Args:
        v: Tensão em Volts (V) - opcional
        i: Corrente em Amperes (A) - opcional
        r: Resistência em Ohms (Ω) - opcional
    
    Returns:
        Dicionário com todas as três grandezas calculadas como tuplas (valor, unidade)
    
    Raises:
        ValueError: Se não forem fornecidos exatamente dois valores
    """
    valores_fornecidos = sum([v is not None, i is not None, r is not None])
    
    if valores_fornecidos != 2:
        raise ValueError("Forneça exatamente dois valores para calcular o terceiro")
    
    if v is None:
        v = calcular_tensao(i, r)
    elif i is None:
        i = calcular_corrente(v, r)
    elif r is None:
        r = calcular_resistencia(v, i)
    
    return {
        'tensao': (v, "V"), 
        'corrente': (i, "A"), 
        'resistencia': (r, "Ω")
    }
