"""
Módulo para processamento em lote de cálculos a partir de arquivo CSV.

Formato do CSV:
    comando,param1,param2,param3,param4
    ohm,v=12,r=470,,
    divider,vin=5.0,r1=10000,r2=4700,
    rc,r=1000,c=10e-6,t=0.02,
    color,laranja,laranja,marrom,dourado
"""

import csv
import os
from typing import List

from .ohm import calcular_ohm
from .divider import calcular_divisor_tensao
from .rc import calcular_rc
from .color_code import decodificar_resistor_4_faixas, formatar_resistencia


def _parsear_param(param: str) -> tuple:
    """
    Converte 'chave=valor' em tupla (chave, valor).
    
    Args:
        param: String no formato 'chave=valor'
    
    Returns:
        Tupla (chave, valor_float)
    
    Raises:
        ValueError: Se o formato for inválido
    """
    if '=' not in param:
        raise ValueError(f"Parâmetro inválido: '{param}'. Use o formato chave=valor")
    chave, valor = param.split('=', 1)
    return chave.strip(), float(valor.strip())


def _processar_linha_ohm(params: List[str]) -> str:
    """Processa uma linha de cálculo de Ohm."""
    kwargs = {}
    for p in params:
        if p.strip():
            chave, valor = _parsear_param(p)
            kwargs[chave] = valor
    
    resultado = calcular_ohm(**kwargs)
    v = resultado['tensao'][0]
    i = resultado['corrente'][0]
    r = resultado['resistencia'][0]
    return f"V={v:.4f}V | I={i:.6f}A | R={r:.4f}Ω"


def _processar_linha_divider(params: List[str]) -> str:
    """Processa uma linha de cálculo de divisor."""
    kwargs = {}
    for p in params:
        if p.strip():
            chave, valor = _parsear_param(p)
            kwargs[chave] = valor
    
    resultado = calcular_divisor_tensao(**kwargs)
    v1 = resultado['v1'][0]
    v2 = resultado['v2'][0]
    return f"V1={v1:.4f}V | V2={v2:.4f}V | Razão={resultado['percentual']:.2f}%"


def _processar_linha_rc(params: List[str]) -> str:
    """Processa uma linha de cálculo RC."""
    kwargs = {}
    for p in params:
        if p.strip():
            chave, valor = _parsear_param(p)
            kwargs[chave] = valor
    
    resultado = calcular_rc(**kwargs)
    return f"τ={resultado['tau']:.6f}s | V(t)={resultado['tensao_t']:.4f}V | {resultado['percentual']:.2f}%"


def _processar_linha_color(params: List[str]) -> str:
    """Processa uma linha de código de cores."""
    cores = [p.strip() for p in params if p.strip()]
    resultado = decodificar_resistor_4_faixas(cores)
    return f"{resultado['formatado']} ±{resultado['tolerancia']}%"


def processar_csv(caminho_entrada: str, caminho_saida: str = "") -> str:
    """
    Lê um arquivo CSV com entradas de cálculo e gera um relatório.
    
    Args:
        caminho_entrada: Caminho do arquivo CSV de entrada
        caminho_saida: Caminho do arquivo de saída (opcional)
    
    Returns:
        String com o relatório completo
    
    Raises:
        FileNotFoundError: Se o arquivo de entrada não existir
        ValueError: Se o formato do CSV for inválido
    """
    if not os.path.exists(caminho_entrada):
        raise FileNotFoundError(f"Arquivo não encontrado: '{caminho_entrada}'")
    
    processadores = {
        'ohm': _processar_linha_ohm,
        'divider': _processar_linha_divider,
        'rc': _processar_linha_rc,
        'color': _processar_linha_color
    }
    
    linhas_resultado = []
    linhas_resultado.append("=" * 60)
    linhas_resultado.append("  RELATÓRIO DE CÁLCULOS - CircuitCalc CLI")
    linhas_resultado.append("=" * 60)
    
    total = 0
    erros = 0
    
    with open(caminho_entrada, 'r', encoding='utf-8') as arquivo:
        leitor = csv.reader(arquivo)
        
        for num_linha, linha in enumerate(leitor, 1):
            # Pula linhas vazias e cabeçalho
            if not linha or linha[0].strip().startswith('#') or linha[0].strip() == 'comando':
                continue
            
            total += 1
            comando = linha[0].strip().lower()
            params = linha[1:] if len(linha) > 1 else []
            
            try:
                if comando not in processadores:
                    raise ValueError(f"Comando desconhecido: '{comando}'")
                
                resultado = processadores[comando](params)
                linhas_resultado.append(f"\n  [{num_linha}] {comando.upper()}")
                linhas_resultado.append(f"      Entrada: {', '.join(p for p in params if p.strip())}")
                linhas_resultado.append(f"      Resultado: {resultado}")
                
            except Exception as e:
                erros += 1
                linhas_resultado.append(f"\n  [{num_linha}] {comando.upper()} ❌ ERRO")
                linhas_resultado.append(f"      Entrada: {', '.join(p for p in params if p.strip())}")
                linhas_resultado.append(f"      Erro: {e}")
    
    linhas_resultado.append("\n" + "=" * 60)
    linhas_resultado.append(f"  Total: {total} cálculos | Sucesso: {total - erros} | Erros: {erros}")
    linhas_resultado.append("=" * 60)
    
    relatorio = '\n'.join(linhas_resultado)
    
    # Salva o relatório se um caminho de saída foi informado
    if caminho_saida:
        with open(caminho_saida, 'w', encoding='utf-8') as arquivo_saida:
            arquivo_saida.write(relatorio)
    
    return relatorio
