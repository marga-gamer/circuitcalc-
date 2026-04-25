"""
Testes para o módulo calculator.
"""

import pytest
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from calculator.ohm import calcular_ohm, calcular_tensao, calcular_corrente, calcular_resistencia
from calculator.divider import calcular_divisor_tensao
from calculator.rc import calcular_rc, calcular_constante_tempo
from calculator.color_code import decodificar_resistor_4_faixas


# ============= TESTES: LEI DE OHM =============

def test_calcular_tensao_basico():
    """Testa cálculo de tensão V = I × R"""
    resultado = calcular_tensao(0.025, 470)
    assert abs(resultado - 11.75) < 0.01


def test_calcular_corrente_basico():
    """Testa cálculo de corrente I = V / R"""
    resultado = calcular_corrente(12, 470)
    assert abs(resultado - 0.0255) < 0.001


def test_calcular_resistencia_basico():
    """Testa cálculo de resistência R = V / I"""
    resultado = calcular_resistencia(12, 0.025)
    assert abs(resultado - 480) < 1


def test_calcular_ohm_faltando_tensao():
    """Testa Lei de Ohm calculando V"""
    resultado = calcular_ohm(i=0.025, r=470)
    assert 'tensao' in resultado
    v_valor = resultado['tensao'][0]
    assert abs(v_valor - 11.75) < 0.01


def test_calcular_ohm_faltando_corrente():
    """Testa Lei de Ohm calculando I"""
    resultado = calcular_ohm(v=12, r=470)
    assert 'corrente' in resultado
    i_valor = resultado['corrente'][0]
    assert abs(i_valor - 0.0255) < 0.001


def test_calcular_ohm_faltando_resistencia():
    """Testa Lei de Ohm calculando R"""
    resultado = calcular_ohm(v=12, i=0.025)
    assert 'resistencia' in resultado
    r_valor = resultado['resistencia'][0]
    assert abs(r_valor - 480) < 1


def test_calcular_ohm_erro_valores_insuficientes():
    """Testa erro quando não fornece 2 valores"""
    with pytest.raises(ValueError, match="exatamente dois valores"):
        calcular_ohm(v=12)


def test_calcular_tensao_erro_valor_negativo():
    """Testa erro com valores negativos"""
    with pytest.raises(ValueError, match="positivos"):
        calcular_tensao(-0.5, 100)


def test_calcular_corrente_erro_resistencia_zero():
    """Testa erro com resistência zero"""
    with pytest.raises(ValueError, match="zero"):
        calcular_corrente(12, 0)


# ============= TESTES: DIVISOR DE TENSÃO =============

def test_divisor_tensao_basico():
    """Testa divisor de tensão básico"""
    resultado = calcular_divisor_tensao(5.0, 10000, 4700)
    v2_valor = resultado['v2'][0]
    assert abs(v2_valor - 1.599) < 0.01
    assert abs(resultado['percentual'] - 31.97) < 0.5


def test_divisor_tensao_resistencias_iguais():
    """Testa divisor com resistências iguais (50%)"""
    resultado = calcular_divisor_tensao(10.0, 1000, 1000)
    v1_valor = resultado['v1'][0]
    v2_valor = resultado['v2'][0]
    assert abs(v1_valor - 5.0) < 0.01
    assert abs(v2_valor - 5.0) < 0.01
    assert abs(resultado['percentual'] - 50.0) < 0.1


def test_divisor_tensao_erro_valores_negativos():
    """Testa erro com valores negativos"""
    with pytest.raises(ValueError, match="positivos"):
        calcular_divisor_tensao(-5, 1000, 1000)


def test_divisor_tensao_erro_resistencias_zero():
    """Testa erro quando ambas resistências são zero"""
    with pytest.raises(ValueError, match="maior que zero"):
        calcular_divisor_tensao(5, 0, 0)


def test_divisor_tensao_erro_vin_zero():
    """Testa erro quando tensão de entrada é zero"""
    with pytest.raises(ValueError, match="maior que zero"):
        calcular_divisor_tensao(0, 1000, 1000)


# ============= TESTES: CIRCUITO RC =============

def test_constante_tempo_basico():
    """Testa cálculo de constante de tempo τ"""
    tau = calcular_constante_tempo(1000, 10e-6)
    assert abs(tau - 0.01) < 0.0001


def test_rc_basico():
    """Testa cálculo completo do circuito RC"""
    resultado = calcular_rc(1000, 10e-6, 0.02)
    assert 'tau' in resultado
    assert 'tensao_t' in resultado
    assert abs(resultado['tau'] - 0.01) < 0.0001


def test_rc_carga_um_tau():
    """Testa tensão após 1τ (deve ser ~63.2% de V0)"""
    resultado = calcular_rc(1000, 10e-6, 0.01, v0=5.0)
    # Em 1τ, V(t) ≈ 63.2% de V0
    assert abs(resultado['percentual'] - 63.2) < 1


def test_constante_tempo_erro_resistencia_zero():
    """Testa erro com resistência zero"""
    with pytest.raises(ValueError, match="maiores que zero"):
        calcular_constante_tempo(0, 10e-6)


def test_rc_erro_capacitancia_negativa():
    """Testa erro com capacitância negativa"""
    with pytest.raises(ValueError, match="maiores que zero"):
        calcular_rc(1000, -10e-6, 0.01)


# ============= TESTES: CÓDIGO DE CORES =============

def test_codigo_cores_basico():
    """Testa decodificação básica: laranja laranja marrom dourado = 330Ω ±5%"""
    resultado = decodificar_resistor_4_faixas(['laranja', 'laranja', 'marrom', 'dourado'])
    assert abs(resultado['resistencia'] - 330) < 0.1
    assert resultado['tolerancia'] == 5


def test_codigo_cores_valores_grandes():
    """Testa resistor de valores altos: amarelo violeta vermelho dourado = 4.7kΩ"""
    resultado = decodificar_resistor_4_faixas(['amarelo', 'violeta', 'vermelho', 'dourado'])
    assert abs(resultado['resistencia'] - 4700) < 0.1
    assert 'kΩ' in resultado['formatado']


def test_codigo_cores_normalizacao():
    """Testa normalização de nomes de cores (ouro -> dourado)"""
    resultado = decodificar_resistor_4_faixas(['verde', 'azul', 'marrom', 'ouro'])
    assert abs(resultado['resistencia'] - 560) < 0.1


def test_codigo_cores_erro_numero_faixas():
    """Testa erro com número incorreto de faixas"""
    with pytest.raises(ValueError, match="4 cores"):
        decodificar_resistor_4_faixas(['laranja', 'laranja', 'marrom'])


def test_codigo_cores_erro_cor_invalida():
    """Testa erro com cor inválida"""
    with pytest.raises(ValueError, match="inválida"):
        decodificar_resistor_4_faixas(['rosa', 'azul', 'marrom', 'dourado'])


def test_codigo_cores_tolerancia_prata():
    """Testa resistor com tolerância prata (10%)"""
    resultado = decodificar_resistor_4_faixas(['marrom', 'preto', 'laranja', 'prateado'])
    assert abs(resultado['resistencia'] - 10000) < 0.1
    assert resultado['tolerancia'] == 10


# ============= TESTES DE FORMATAÇÃO =============

def test_formato_ohms():
    """Testa formatação em Ohms"""
    from calculator.color_code import formatar_resistencia
    assert 'Ω' in formatar_resistencia(470)
    assert '470' in formatar_resistencia(470)


def test_formato_kilohms():
    """Testa formatação em kΩ"""
    from calculator.color_code import formatar_resistencia
    resultado = formatar_resistencia(4700)
    assert 'kΩ' in resultado
    assert '4.70' in resultado


def test_formato_megohms():
    """Testa formatação em MΩ"""
    from calculator.color_code import formatar_resistencia
    resultado = formatar_resistencia(1000000)
    assert 'MΩ' in resultado
    assert '1.00' in resultado
