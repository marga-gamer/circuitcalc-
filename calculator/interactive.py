"""
Módulo de modo interativo da CircuitCalc CLI.
Exibe um menu no terminal quando o programa é executado sem argumentos.
"""

import sys
from typing import Optional

from .ohm import calcular_ohm
from .divider import calcular_divisor_tensao
from .rc import calcular_rc
from .color_code import decodificar_resistor_4_faixas, formatar_resistencia


def ler_float(mensagem: str) -> Optional[float]:
    """
    Lê um float do usuário com tratamento de erro.
    
    Args:
        mensagem: Texto exibido ao usuário
    
    Returns:
        Valor float digitado ou None se vazio
    """
    while True:
        entrada = input(mensagem).strip()
        if entrada == '' or entrada.lower() == 'n':
            return None
        try:
            return float(entrada)
        except ValueError:
            print("  ⚠ Valor inválido. Digite um número ou deixe vazio para pular.")


def ler_float_obrigatorio(mensagem: str) -> float:
    """
    Lê um float obrigatório do usuário.
    
    Args:
        mensagem: Texto exibido ao usuário
    
    Returns:
        Valor float digitado
    """
    while True:
        entrada = input(mensagem).strip()
        try:
            return float(entrada)
        except ValueError:
            print("  ⚠ Valor inválido. Digite um número.")


def menu_ohm() -> dict:
    """Executa o cálculo interativo da Lei de Ohm."""
    print("\n  ─── Lei de Ohm (V = I × R) ───")
    print("  Informe dois valores e deixe o terceiro vazio.\n")
    
    v = ler_float("  Tensão (V) [vazio para calcular]: ")
    i = ler_float("  Corrente (A) [vazio para calcular]: ")
    r = ler_float("  Resistência (Ω) [vazio para calcular]: ")
    
    resultado = calcular_ohm(v=v, i=i, r=r)
    
    v_val = resultado['tensao'][0]
    i_val = resultado['corrente'][0]
    r_val = resultado['resistencia'][0]
    
    print(f"\n  ✔ Tensão:      {v_val:.4f} V")
    print(f"  ✔ Corrente:    {i_val:.6f} A")
    print(f"  ✔ Resistência: {r_val:.4f} Ω")
    
    return resultado


def menu_divider() -> dict:
    """Executa o cálculo interativo do divisor de tensão."""
    print("\n  ─── Divisor de Tensão ───\n")
    
    vin = ler_float_obrigatorio("  Tensão de entrada Vin (V): ")
    r1 = ler_float_obrigatorio("  Resistência R1 (Ω): ")
    r2 = ler_float_obrigatorio("  Resistência R2 (Ω): ")
    
    resultado = calcular_divisor_tensao(vin, r1, r2)
    
    v1_val = resultado['v1'][0]
    v2_val = resultado['v2'][0]
    
    print(f"\n  ✔ V1 (sobre R1): {v1_val:.4f} V")
    print(f"  ✔ V2 (sobre R2): {v2_val:.4f} V")
    print(f"  ✔ Razão:         {resultado['percentual']:.2f} %")
    
    return resultado


def menu_rc() -> dict:
    """Executa o cálculo interativo do circuito RC."""
    print("\n  ─── Circuito RC ───\n")
    
    r = ler_float_obrigatorio("  Resistência R (Ω): ")
    c = ler_float_obrigatorio("  Capacitância C (F) [ex: 10e-6 para 10µF]: ")
    t = ler_float_obrigatorio("  Tempo t (s): ")
    
    resultado = calcular_rc(r, c, t)
    
    print(f"\n  ✔ τ (tau):     {resultado['tau']:.6f} s")
    print(f"  ✔ V(t):        {resultado['tensao_t']:.4f} V")
    print(f"  ✔ Percentual:  {resultado['percentual']:.2f} %")
    
    return resultado


def menu_color() -> dict:
    """Executa a decodificação interativa de código de cores."""
    print("\n  ─── Código de Cores (4 faixas) ───")
    print("  Cores: preto, marrom, vermelho, laranja, amarelo,")
    print("         verde, azul, violeta, cinza, branco, dourado, prateado\n")
    
    faixa1 = input("  Faixa 1 (dígito): ").strip()
    faixa2 = input("  Faixa 2 (dígito): ").strip()
    faixa3 = input("  Faixa 3 (multiplicador): ").strip()
    faixa4 = input("  Faixa 4 (tolerância): ").strip()
    
    resultado = decodificar_resistor_4_faixas([faixa1, faixa2, faixa3, faixa4])
    
    print(f"\n  ✔ Resistência: {resultado['formatado']}")
    print(f"  ✔ Valor exato: {resultado['resistencia']:.2f} Ω")
    print(f"  ✔ Tolerância:  ±{resultado['tolerancia']}%")
    
    return resultado


def menu_potencia() -> dict:
    """Calcula a potência dissipada com aviso de limite."""
    print("\n  ─── Potência Dissipada no Resistor ───\n")
    
    v = ler_float_obrigatorio("  Tensão sobre o resistor (V): ")
    i = ler_float_obrigatorio("  Corrente no resistor (A): ")
    limite = ler_float("  Limite de potência (W) [vazio = 0.25W]: ")
    
    if limite is None:
        limite = 0.25
    
    potencia = v * i
    
    print(f"\n  ✔ Potência dissipada: {potencia:.4f} W ({potencia * 1000:.2f} mW)")
    
    if potencia > limite:
        print(f"  ⚠ AVISO: Potência ({potencia:.4f} W) EXCEDE o limite de {limite:.4f} W!")
        print(f"  ⚠ O resistor pode superaquecer ou queimar.")
    else:
        print(f"  ✔ Dentro do limite ({potencia:.4f} W ≤ {limite:.4f} W)")
    
    return {'potencia': potencia, 'limite': limite, 'excede': potencia > limite}


def executar_modo_interativo() -> None:
    """
    Executa o modo interativo com menu no terminal.
    Loop contínuo até o usuário escolher sair.
    """
    print("╔════════════════════════════════════════╗")
    print("║        CircuitCalc CLI - Menu          ║")
    print("║  Calculadora de Engenharia Elétrica    ║")
    print("╚════════════════════════════════════════╝")
    
    opcoes = {
        '1': ('Lei de Ohm (V=I×R)', menu_ohm),
        '2': ('Divisor de Tensão', menu_divider),
        '3': ('Circuito RC', menu_rc),
        '4': ('Código de Cores', menu_color),
        '5': ('Potência Dissipada', menu_potencia),
        '0': ('Sair', None)
    }
    
    while True:
        print("\n┌─────────────────────────────────┐")
        for chave, (nome, _) in opcoes.items():
            print(f"│  [{chave}] {nome:<27} │")
        print("└─────────────────────────────────┘")
        
        escolha = input("\n  Escolha uma opção: ").strip()
        
        if escolha == '0':
            print("\n  Até mais! ⚡")
            break
        
        if escolha not in opcoes:
            print("  ⚠ Opção inválida. Tente novamente.")
            continue
        
        nome, funcao = opcoes[escolha]
        
        try:
            funcao()
        except ValueError as e:
            print(f"\n  ❌ Erro: {e}")
        except KeyboardInterrupt:
            print("\n\n  Operação cancelada.")
        
        input("\n  Pressione Enter para continuar...")
