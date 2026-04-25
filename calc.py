    #!/usr/bin/env python3
"""
CircuitCalc CLI - Ferramenta de cálculos de engenharia elétrica.

Uso:
    python calc.py ohm --v 12 --r 470
    python calc.py divider --vin 5.0 --r1 10000 --r2 4700
    python calc.py rc --r 1000 --c 10e-6 --t 0.02
    python calc.py color --bands laranja laranja marrom dourado
    python calc.py power --v 12 --i 0.025 --limit 0.5
    python calc.py batch --input entradas.csv --output relatorio.txt
    python calc.py history
    python calc.py              (modo interativo)
"""

import argparse
import sys

from calculator.ohm import calcular_ohm
from calculator.divider import calcular_divisor_tensao
from calculator.rc import calcular_rc
from calculator.color_code import decodificar_resistor_4_faixas
from calculator.power import calcular_potencia, verificar_limite_potencia
from calculator.history import registrar_calculo, listar_historico, limpar_historico
from calculator.batch import processar_csv


def cmd_ohm(args) -> None:
    """Executa o comando de Lei de Ohm."""
    try:
        resultado = calcular_ohm(v=args.v, i=args.i, r=args.r)
        
        v_valor = resultado['tensao'][0]
        i_valor = resultado['corrente'][0]
        r_valor = resultado['resistencia'][0]
        
        print("╔════════════════════════════════════╗")
        print("║         LEI DE OHM (V=I×R)         ║")
        print("╠════════════════════════════════════╣")
        print(f"║ Tensão (V):      {v_valor:>12.4f} V    ║")
        print(f"║ Corrente (I):    {i_valor:>12.4f} A    ║")
        print(f"║ Resistência (R): {r_valor:>12.4f} Ω    ║")
        print("╚════════════════════════════════════╝")
        
        registrar_calculo('ohm', {'v': args.v, 'i': args.i, 'r': args.r}, resultado)
        
    except ValueError as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_divider(args) -> None:
    """Executa o comando de divisor de tensão."""
    try:
        resultado = calcular_divisor_tensao(args.vin, args.r1, args.r2)
        
        v1_valor = resultado['v1'][0]
        v2_valor = resultado['v2'][0]
        
        print("╔════════════════════════════════════╗")
        print("║       DIVISOR DE TENSÃO            ║")
        print("╠════════════════════════════════════╣")
        print(f"║ Vin:  {args.vin:>12.4f} V              ║")
        print(f"║ R1:   {args.r1:>12.4f} Ω              ║")
        print(f"║ R2:   {args.r2:>12.4f} Ω              ║")
        print("╠════════════════════════════════════╣")
        print(f"║ V1:   {v1_valor:>12.4f} V              ║")
        print(f"║ V2:   {v2_valor:>12.4f} V              ║")
        print(f"║ Razão: {resultado['percentual']:>11.2f} %             ║")
        print("╚════════════════════════════════════╝")
        
        registrar_calculo('divider', {'vin': args.vin, 'r1': args.r1, 'r2': args.r2}, resultado)
        
    except ValueError as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_rc(args) -> None:
    """Executa o comando de circuito RC."""
    try:
        resultado = calcular_rc(args.r, args.c, args.t)
        
        print("╔════════════════════════════════════╗")
        print("║         CIRCUITO RC                ║")
        print("╠════════════════════════════════════╣")
        print(f"║ R: {args.r:>12.4f} Ω                  ║")
        print(f"║ C: {args.c:>12.4e} F                  ║")
        print(f"║ τ (tau): {resultado['tau']:>12.6f} s            ║")
        print("╠════════════════════════════════════╣")
        print(f"║ Tempo (t): {args.t:>10.6f} s            ║")
        print(f"║ V(t): {resultado['tensao_t']:>15.4f} V            ║")
        print(f"║ Percentual: {resultado['percentual']:>9.2f} %            ║")
        print("╚════════════════════════════════════╝")
        
        registrar_calculo('rc', {'r': args.r, 'c': args.c, 't': args.t}, resultado)
        
    except ValueError as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_color(args) -> None:
    """Executa o comando de código de cores."""
    try:
        resultado = decodificar_resistor_4_faixas(args.bands)
        
        print("╔════════════════════════════════════╗")
        print("║    CÓDIGO DE CORES (4 FAIXAS)      ║")
        print("╠════════════════════════════════════╣")
        
        for i, cor in enumerate(resultado['faixas'], 1):
            print(f"║ Faixa {i}: {cor:<26}║")
        
        print("╠════════════════════════════════════╣")
        print(f"║ Resistência: {resultado['formatado']:>21} ║")
        print(f"║ Tolerância: {resultado['tolerancia']:>20.2f} % ║")
        print(f"║ Valor exato: {resultado['resistencia']:>19.2f} Ω ║")
        print("╚════════════════════════════════════╝")
        
        registrar_calculo('color', {'bands': args.bands}, resultado)
        
    except ValueError as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_power(args) -> None:
    """Executa o comando de potência dissipada."""
    try:
        resultado = calcular_potencia(v=args.v or 0, i=args.i or 0, r=args.r or 0)
        limite = verificar_limite_potencia(resultado['potencia'], args.limit)
        
        print("╔════════════════════════════════════╗")
        print("║     POTÊNCIA DISSIPADA             ║")
        print("╠════════════════════════════════════╣")
        print(f"║ Tensão:      {resultado['tensao']:>12.4f} V       ║")
        print(f"║ Corrente:    {resultado['corrente']:>12.6f} A       ║")
        print(f"║ Resistência: {resultado['resistencia']:>12.4f} Ω       ║")
        print("╠════════════════════════════════════╣")
        print(f"║ Potência: {resultado['potencia']:>12.4f} W          ║")
        print(f"║ Limite:   {args.limit:>12.4f} W          ║")
        
        if limite['excede']:
            print("║                                    ║")
            print("║ ⚠  ATENÇÃO: POTÊNCIA EXCEDIDA!     ║")
            print("║ ⚠  Risco de superaquecimento!      ║")
        else:
            print(f"║ Margem:   {limite['margem']:>11.2f} %          ║")
            print("║ ✔ Dentro do limite seguro           ║")
        
        print("╚════════════════════════════════════╝")
        
        registrar_calculo('power', {'v': args.v, 'i': args.i, 'r': args.r, 'limit': args.limit}, resultado)
        
    except ValueError as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_batch(args) -> None:
    """Executa processamento em lote de um arquivo CSV."""
    try:
        relatorio = processar_csv(args.input, args.output or "")
        print(relatorio)
        
        if args.output:
            print(f"\n  ✔ Relatório salvo em: {args.output}")
        
    except FileNotFoundError as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao processar CSV: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_history(args) -> None:
    """Exibe ou limpa o histórico de cálculos."""
    if args.clear:
        limpar_historico()
        print("  ✔ Histórico limpo com sucesso.")
    else:
        print(listar_historico(limite=args.n))


def main():
    """Função principal da CLI."""
    parser = argparse.ArgumentParser(
        description='CircuitCalc - Calculadora de engenharia elétrica',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python calc.py ohm --v 12 --r 470
  python calc.py ohm --v 12 --i 0.025
  python calc.py divider --vin 5.0 --r1 10000 --r2 4700
  python calc.py rc --r 1000 --c 10e-6 --t 0.02
  python calc.py color --bands laranja laranja marrom dourado
  python calc.py power --v 12 --i 0.025 --limit 0.5
  python calc.py batch --input entradas.csv --output relatorio.txt
  python calc.py history
  python calc.py history --clear
  python calc.py                     (modo interativo)
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comando a executar')
    
    # Comando: ohm
    parser_ohm = subparsers.add_parser('ohm', help='Lei de Ohm (V=I×R)')
    parser_ohm.add_argument('--v', type=float, help='Tensão em Volts')
    parser_ohm.add_argument('--i', type=float, help='Corrente em Amperes')
    parser_ohm.add_argument('--r', type=float, help='Resistência em Ohms')
    parser_ohm.set_defaults(func=cmd_ohm)
    
    # Comando: divider
    parser_divider = subparsers.add_parser('divider', help='Divisor de tensão')
    parser_divider.add_argument('--vin', type=float, required=True, help='Tensão de entrada em Volts')
    parser_divider.add_argument('--r1', type=float, required=True, help='Resistência R1 em Ohms')
    parser_divider.add_argument('--r2', type=float, required=True, help='Resistência R2 em Ohms')
    parser_divider.set_defaults(func=cmd_divider)
    
    # Comando: rc
    parser_rc = subparsers.add_parser('rc', help='Circuito RC')
    parser_rc.add_argument('--r', type=float, required=True, help='Resistência em Ohms')
    parser_rc.add_argument('--c', type=float, required=True, help='Capacitância em Farads')
    parser_rc.add_argument('--t', type=float, required=True, help='Tempo em segundos')
    parser_rc.set_defaults(func=cmd_rc)
    
    # Comando: color
    parser_color = subparsers.add_parser('color', help='Código de cores de resistor')
    parser_color.add_argument('--bands', nargs=4, required=True, 
                             help='4 cores do resistor (ex: laranja laranja marrom dourado)')
    parser_color.set_defaults(func=cmd_color)
    
    # Comando: power (EXTRA)
    parser_power = subparsers.add_parser('power', help='Potência dissipada no resistor')
    parser_power.add_argument('--v', type=float, help='Tensão em Volts')
    parser_power.add_argument('--i', type=float, help='Corrente em Amperes')
    parser_power.add_argument('--r', type=float, help='Resistência em Ohms')
    parser_power.add_argument('--limit', type=float, default=0.25, 
                             help='Limite de potência em Watts (padrão: 0.25)')
    parser_power.set_defaults(func=cmd_power)
    
    # Comando: batch (EXTRA)
    parser_batch = subparsers.add_parser('batch', help='Processamento em lote via CSV')
    parser_batch.add_argument('--input', required=True, help='Arquivo CSV de entrada')
    parser_batch.add_argument('--output', help='Arquivo de saída do relatório (opcional)')
    parser_batch.set_defaults(func=cmd_batch)
    
    # Comando: history (EXTRA)
    parser_history = subparsers.add_parser('history', help='Histórico de cálculos')
    parser_history.add_argument('--n', type=int, default=10, help='Número de registros a exibir')
    parser_history.add_argument('--clear', action='store_true', help='Limpar o histórico')
    parser_history.set_defaults(func=cmd_history)
    
    # Parse dos argumentos
    args = parser.parse_args()
    
    # Se nenhum comando → modo interativo
    if not args.command:
        from calculator.interactive import executar_modo_interativo
        executar_modo_interativo()
        return
    
    # Executa o comando
    args.func(args)


if __name__ == '__main__':
    main()
