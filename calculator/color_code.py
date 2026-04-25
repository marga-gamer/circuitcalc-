"""
Módulo para decodificação de código de cores de resistores (4 faixas).
Como funciona:
RESISTOR:
  ┌─────────────┐
  │ ││││        │
  │ ││││        │  
  └─────────────┘
    1234

Faixa 1: Primeiro dígito
Faixa 2: Segundo dígito  
Faixa 3: Multiplicador (quantos zeros)
Faixa 4: Tolerância (precisão ±%)
"""

from typing import List, Tuple


# Mapeamento de cores para valores
CORES_DIGITO = {
    'preto': 0,
    'marrom': 1,
    'vermelho': 2,
    'laranja': 3,
    'amarelo': 4,
    'verde': 5,
    'azul': 6,
    'violeta': 7,
    'cinza': 8,
    'branco': 9
}

CORES_MULTIPLICADOR = {
    'preto': 1,
    'marrom': 10,
    'vermelho': 100,
    'laranja': 1000,
    'amarelo': 10000,
    'verde': 100000,
    'azul': 1000000,
    'violeta': 10000000,
    'cinza': 100000000,
    'branco': 1000000000,
    'dourado': 0.1, 
    'prateado': 0.01
}

CORES_TOLERANCIA = {
    'marrom': 1,
    'vermelho': 2,
    'verde': 0.5,
    'azul': 0.25,
    'violeta': 0.1,
    'cinza': 0.05,
    'dourado': 5,
    'prateado': 10,
    'sem_faixa': 20
}


def normalizar_cor(cor: str) -> str:
    """
    Normaliza o nome da cor (remove acentos, converte para minúsculas).
    
    Args:
        cor: Nome da cor
    
    Returns:
        Nome da cor normalizado
    """
    # Remove espaços e converte para minúsculas
    cor = cor.strip().lower()
    
    # Mapeamento de variações comuns
    variacoes = {
        'ouro': 'dourado',
        'gold': 'dourado',
        'prata': 'prateado',
        'silver': 'prateado',
        'roxo': 'violeta',
        'purple': 'violeta',
        'gray': 'cinza',
        'grey': 'cinza'
    }
    
    return variacoes.get(cor, cor)


def decodificar_resistor_4_faixas(faixas: List[str]) -> dict:
    """
    Decodifica o valor de um resistor de 4 faixas.
    
    Argumentos:
        faixas: Lista com 4 cores [digito1, digito2, multiplicador, tolerancia]
    
    Returns:
        Dicionário com resistência em Ohms, tolerância em % e formatação legível
    
    Raises:
        ValueError: Se as faixas forem inválidas
    """
    if len(faixas) != 4:
        raise ValueError(f"Resistor de 4 faixas requer exatamente 4 cores, recebeu {len(faixas)}")
    
    # Normaliza as cores
    faixas_norm = [normalizar_cor(f) for f in faixas]
    cor1, cor2, cor_mult, cor_tol = faixas_norm
    
    # Valida e obtém os dígitos
    if cor1 not in CORES_DIGITO:
        raise ValueError(f"Cor inválida para primeira faixa: '{faixas[0]}'")
    if cor2 not in CORES_DIGITO:
        raise ValueError(f"Cor inválida para segunda faixa: '{faixas[1]}'")
    
    digito1 = CORES_DIGITO[cor1]
    digito2 = CORES_DIGITO[cor2]
    
    # Valida e obtém o multiplicador
    if cor_mult not in CORES_MULTIPLICADOR:
        raise ValueError(f"Cor inválida para multiplicador: '{faixas[2]}'")
    
    multiplicador = CORES_MULTIPLICADOR[cor_mult]
    
    # Valida e obtém a tolerância
    if cor_tol not in CORES_TOLERANCIA:
        raise ValueError(f"Cor inválida para tolerância: '{faixas[3]}'")
    
    tolerancia = CORES_TOLERANCIA[cor_tol]
    
    # Calcula o valor
    valor_base = (digito1 * 10 + digito2)
    resistencia = valor_base * multiplicador
    
    return {
        'resistencia': resistencia,
        'tolerancia': tolerancia,
        'formatado': formatar_resistencia(resistencia),
        'faixas': faixas
    }


def formatar_resistencia(valor: float) -> str:
    """
    Formata o valor da resistência com unidade apropriada (Ω, kΩ, MΩ).
    
    Args:
        valor: Resistência em Ohms
    
    Returns:
        String formatada com unidade
    """
    if valor >= 1_000_000:
        return f"{valor / 1_000_000:.2f} MΩ"
    elif valor >= 1_000:
        return f"{valor / 1_000:.2f} kΩ"
    else:
        return f"{valor:.2f} Ω"
