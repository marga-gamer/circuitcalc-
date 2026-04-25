# CircuitCalc CLI

Ferramenta de linha de comando em Python para cálculos essenciais de engenharia elétrica.

## Instalação

1. Clone o repositório:
```bash
git clone <seu-repositorio>
cd circuitcalc
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

### Lei de Ohm (V = I × R)

Informe dois dos três valores para calcular o terceiro:

```bash
python calc.py ohm --v 12 --r 470
python calc.py ohm --v 12 --i 0.025
python calc.py ohm --i 0.025 --r 470
```

### Divisor de Tensão

```bash
python calc.py divider --vin 5.0 --r1 10000 --r2 4700
```

### Circuito RC

Calcula constante de tempo (τ) e tensão no capacitor em um dado tempo:

```bash
python calc.py rc --r 1000 --c 10e-6 --t 0.02
```

**Parâmetros:**
- `--r`: Resistência em Ohms (Ω)
- `--c`: Capacitância em Farads (F) - use notação científica (ex: 10e-6 = 10µF)
- `--t`: Tempo em segundos (s)

### Código de Cores de Resistores (4 faixas)

```bash
python calc.py color --bands laranja laranja marrom dourado
```

**Cores suportadas:**
- Dígitos: preto, marrom, vermelho, laranja, amarelo, verde, azul, violeta, cinza, branco
- Multiplicador: mesmas cores + dourado, prateado
- Tolerância: marrom (1%), vermelho (2%), verde (0.5%), azul (0.25%), violeta (0.1%), cinza (0.05%), dourado (5%), prateado (10%)

**Variações aceitas:**
- ouro/gold → dourado
- prata/silver → prateado
- roxo/purple → violeta

## Features Extras

### Verificador de Potência Dissipada

Calcula a potência dissipada em um resistor e alerta se exceder o limite:

```bash
python calc.py power --v 12 --i 0.025 --limit 0.5
python calc.py power --v 5 --r 100 --limit 0.25
```

### Modo Interativo

Execute sem argumentos para abrir um menu interativo:

```bash
python calc.py
```

O menu permite executar qualquer cálculo sem precisar lembrar os argumentos da CLI.

### Processamento em Lote (CSV)

Processe múltiplos cálculos de uma vez a partir de um arquivo CSV:

```bash
python calc.py batch --input exemplo_entradas.csv
python calc.py batch --input entradas.csv --output relatorio.txt
```

Formato do CSV:
```csv
comando,param1,param2,param3,param4
ohm,v=12,r=470,,
divider,vin=5.0,r1=10000,r2=4700,
rc,r=1000,c=10e-6,t=0.02,
color,laranja,laranja,marrom,dourado
```

### Histórico de Cálculos

Todos os cálculos são salvos automaticamente em `historico.json`:

```bash
python calc.py history           # Mostra os últimos 10 cálculos
python calc.py history --n 20    # Mostra os últimos 20
python calc.py history --clear   # Limpa o histórico
```

## Testes

Execute os testes com pytest:

```bash
pytest tests/test_calculator.py -v
```

## Estrutura do Projeto

```
circuitcalc/
├── calc.py                        # Entry point - CLI principal
├── calculator/                    # Módulo de cálculos
│   ├── __init__.py
│   ├── ohm.py                    # Lei de Ohm
│   ├── divider.py                # Divisor de tensão
│   ├── rc.py                     # Circuito RC
│   ├── color_code.py             # Código de cores
│   ├── power.py                  # Potência dissipada (extra)
│   ├── interactive.py            # Modo interativo (extra)
│   ├── batch.py                  # Processamento CSV (extra)
│   └── history.py                # Histórico de cálculos (extra)
├── tests/
│   └── test_calculator.py        # Testes com pytest
├── exemplo_entradas.csv          # CSV de exemplo para batch
├── requirements.txt              # Dependências
└── README.md                     # Este arquivo
```

## Requisitos

- Python 3.10+
- pytest (para testes)
- Nenhuma biblioteca externa para a lógica de cálculo

## Commits Semânticos

Este projeto utiliza commits semânticos:
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `test:` Adição ou modificação de testes
- `docs:` Documentação
- `refactor:` Refatoração de código

## Autor

Henrique Margarido

## Licença

Projeto educacional - PixelPulseLab
