"""
Módulo para cálculo de potência dissipada em resistores.
P = V × I = V² / R = I² × R
"""


def calcular_potencia(v: float = 0, i: float = 0, r: float = 0) -> dict:
    """
    Calcula a potência dissipada em um resistor.
    Aceita qualquer combinação de dois valores (V, I, R).
    
    Args:
        v: Tensão sobre o resistor em Volts (V)
        i: Corrente no resistor em Amperes (A)
        r: Resistência em Ohms (Ω)
    
    Returns:
        Dicionário com potência, tensão, corrente e resistência
    
    Raises:
        ValueError: Se os valores forem insuficientes ou inválidos
    """
    if v < 0 or i < 0 or r < 0:
        raise ValueError("Todos os valores devem ser positivos")
    
    # Calcula a potência com os dados disponíveis
    if v > 0 and i > 0:
        potencia = v * i
        if r == 0:
            r = v / i
    elif v > 0 and r > 0:
        potencia = (v ** 2) / r
        i = v / r
    elif i > 0 and r > 0:
        potencia = (i ** 2) * r
        v = i * r
    else:
        raise ValueError("Forneça pelo menos dois valores (V, I ou R) maiores que zero")
    
    return {
        'potencia': potencia,
        'tensao': v,
        'corrente': i,
        'resistencia': r
    }


def verificar_limite_potencia(potencia: float, limite: float = 0.25) -> dict:
    """
    Verifica se a potência excede o limite do resistor.
    
    Args:
        potencia: Potência calculada em Watts (W)
        limite: Potência máxima do resistor em Watts (padrão: 0.25W)
    
    Returns:
        Dicionário com status e margem de segurança
    """
    if limite <= 0:
        raise ValueError("Limite de potência deve ser maior que zero")
    
    excede = potencia > limite
    margem = ((limite - potencia) / limite) * 100
    
    return {
        'potencia': potencia,
        'limite': limite,
        'excede': excede,
        'margem': margem
    }
