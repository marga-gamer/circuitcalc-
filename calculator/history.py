"""
Módulo para salvar e consultar histórico de cálculos em arquivo JSON.
Os resultados são salvos em 'historico.json' no diretório do projeto.
"""

import json
import os
from datetime import datetime
from typing import Any, List


ARQUIVO_HISTORICO = "historico.json"


def _carregar_historico() -> List[dict]:
    """
    Carrega o histórico do arquivo JSON.
    
    Returns:
        Lista de registros de cálculos anteriores
    """
    if not os.path.exists(ARQUIVO_HISTORICO):
        return []
    
    try:
        with open(ARQUIVO_HISTORICO, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _salvar_historico(historico: List[dict]) -> None:
    """
    Salva o histórico no arquivo JSON.
    
    Args:
        historico: Lista de registros para salvar
    """
    with open(ARQUIVO_HISTORICO, 'w', encoding='utf-8') as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)


def _serializar_resultado(resultado: dict) -> dict:
    """
    Converte tuplas (valor, unidade) em dicts para serialização JSON.
    
    Args:
        resultado: Dicionário com resultados do cálculo
    
    Returns:
        Dicionário serializável em JSON
    """
    serializado = {}
    for chave, valor in resultado.items():
        if isinstance(valor, tuple) and len(valor) == 2:
            serializado[chave] = {'valor': valor[0], 'unidade': valor[1]}
        else:
            serializado[chave] = valor
    return serializado


def registrar_calculo(comando: str, entrada: dict, resultado: dict) -> None:
    """
    Registra um cálculo no histórico.
    
    Args:
        comando: Nome do comando executado (ohm, divider, rc, color)
        entrada: Dicionário com os parâmetros de entrada
        resultado: Dicionário com os resultados do cálculo
    """
    historico = _carregar_historico()
    
    registro = {
        'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'comando': comando,
        'entrada': entrada,
        'resultado': _serializar_resultado(resultado)
    }
    
    historico.append(registro)
    _salvar_historico(historico)


def listar_historico(limite: int = 10) -> str:
    """
    Lista os últimos cálculos do histórico formatados.
    
    Args:
        limite: Número máximo de registros a exibir
    
    Returns:
        String formatada com o histórico
    """
    historico = _carregar_historico()
    
    if not historico:
        return "  Nenhum cálculo registrado ainda."
    
    ultimos = historico[-limite:]
    linhas = []
    linhas.append("╔════════════════════════════════════════╗")
    linhas.append("║       HISTÓRICO DE CÁLCULOS            ║")
    linhas.append("╠════════════════════════════════════════╣")
    
    for i, reg in enumerate(reversed(ultimos), 1):
        linhas.append(f"║ {i}. [{reg['data']}]")
        linhas.append(f"║    Comando: {reg['comando'].upper()}")
        
        # Formata entrada
        entrada_str = ', '.join(f"{k}={v}" for k, v in reg['entrada'].items() if v is not None)
        linhas.append(f"║    Entrada: {entrada_str}")
        
        # Formata resultado resumido
        resultado_parts = []
        for k, v in reg['resultado'].items():
            if isinstance(v, dict) and 'valor' in v:
                resultado_parts.append(f"{k}={v['valor']:.4f}{v['unidade']}")
            elif isinstance(v, (int, float)):
                resultado_parts.append(f"{k}={v}")
        
        if resultado_parts:
            linhas.append(f"║    Resultado: {', '.join(resultado_parts[:3])}")
        
        linhas.append("║")
    
    linhas.append(f"║  Total de registros: {len(historico)}")
    linhas.append("╚════════════════════════════════════════╝")
    
    return '\n'.join(linhas)


def limpar_historico() -> None:
    """Remove todos os registros do histórico."""
    if os.path.exists(ARQUIVO_HISTORICO):
        os.remove(ARQUIVO_HISTORICO)
