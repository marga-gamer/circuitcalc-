"""
Módulo para cálculo de divisor de tensão.
V2 = Vin × (R2 / (R1 + R2)) ou V1 = Vin × (R1 / (R1 + R2))
"""


def calcular_divisor_tensao(vin: float, r1: float, r2: float) -> dict:
    """
    Calcula a tensão de saída de um divisor de tensão resistivo.
    
    Args:
        vin: Tensão de entrada em Volts (V)
        r1: Resistência um em Ohms (Ω)
        r2: Resistência dois em Ohms (Ω)
    
    Returns:
        Dicionário com tensões em cada resistor e razão de divisão
    
    Raises:
        ValueError: Se alguma resistencia for negativa, se resistências forem zero, ou se vin é zero
    """
    if vin < 0 or r1 < 0 or r2 < 0:
        raise ValueError("Todos os valores devem ser positivos")
    
    if r1 == 0 and r2 == 0:
        raise ValueError("Pelo menos uma resistência deve ser maior que zero")
    
    if vin == 0:
        raise ValueError("A tensão deve ser maior que zero")
    
    razao = r2 / (r1 + r2) if (r1 + r2) > 0 else 0
    v2 = vin * razao
    v1 = vin - v2
    
    return {
        'v2': (v2, "V"),
        'v1': (v1, "V"), 
        'razao': razao,
        'percentual': razao * 100
    }
