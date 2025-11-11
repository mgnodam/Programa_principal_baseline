# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 11:02:44 2025

@author: ITA
"""

# ---------------------------------------------------------------------------
#  car an_inputs.py
# ---------------------------------------------------------------------------

import pandas as pd

def sheet_to_dict(url):
    """
    Lê a primeira aba de uma planilha Google Sheets (ou CSV online)
    e converte a primeira coluna em chaves e a segunda em valores.
    Converte valores numéricos para float automaticamente.
    """

    # tenta ler CSV diretamente (funciona com links do Google Sheets)
    df = pd.read_csv(url)

    # pega as duas primeiras colunas
    colunas = df.columns[:2]

    def try_float(x):
        """Converte para float se possível, senão mantém o original."""
        try:
            # remove vírgula decimal se houver (ex: "1,5" -> "1.5")
            return float(str(x).replace(",", "."))
        except (ValueError, TypeError):
            return x

    # aplica a conversão valor a valor
    chaves = df[colunas[0]]
    valores = df[colunas[1]].apply(try_float)

    # monta o dicionário
    return dict(zip(chaves, valores))

# --- parâmetros operacionais compartilhados -------------------------------

shared_data = sheet_to_dict("https://docs.google.com/spreadsheets/d/100af-Tr-Wuz38QzfV7mmlbSN4jkKrwjEEd0AOOVYKas/gviz/tq?tqx=out:csv")
shared = dict(
    annual_hours     = shared_data["annual_hours"], # Quantidade de horas de bloco que a aeronave voa em um ano de operação. 
                            # Usada como divisor para transformar custos anuais (salários, seguro, capital) em custos por hora ou por milha.
    block_time_hr    = shared_data["block_time_hr"], # Duração média de um ciclo “bloco-bloco”: do acionamento de calços antes da saída (off-blocks) até 
                            # a recolocação dos calços após o pouso (on-blocks). Inclui taxi, decolagem, subida, cruzeiro, descida, aproximação, 
                            # arremate se ocorrer, taxi de chegada e eventuais esperas.
    block_speed_kts  = shared_data["block_speed_kts"], # Velocidade média “de bloco”, obtida dividindo a distância bloco (nm) pelo tempo de bloco. Combina cruzeiro mais todas as fases de voo, 
                            # sendo menor do que a velocidade de cruzeiro pura. Necessária para converter custos por hora em custos por milha náutica.
    distance_km      = shared_data["distance_km"], # Distância geográfica da rota de estudo, medida em quilômetros. Se o modelo usa milhas náuticas internamente, converte-se por 1 nm = 1,852 km.
                            # Serve para estimar consumo e para dividir custos de viagem.
    usd_per_brl      = shared_data["usd_per_brl"],# Taxa de câmbio utilizada para converter custos cotados em reais (BRL) para dólares americanos (USD), unidade tradicional nos estudos DOC de Roskam.
    preco_aeronave   = shared_data["preco_aeronave"], # Valor de mercado ou custo de aquisição da aeronave (airframe + motores no estado considerado). 
                                  # Entra no cálculo de depreciação, seguro e custo de capital (juros ou lease).
    num_motores      = shared_data["num_motores"],  # Número total de motores instalados. Impacta consumo de óleo (motores a turbina), manutenção de grupo moto-propulsor e,
                           # em estudos híbridos, o dimensionamento de geradores e sistemas auxiliares.
    )

flight_data = sheet_to_dict("https://docs.google.com/spreadsheets/d/1Z-e2u0DK4LDfgLZaUOrdi2H1LU-JKsL-cKYV5SuhU-Q/gviz/tq?tqx=out:csv")
flight = dict(
        tipo                  = flight_data["tipo"],                # Tipo da aeronave (Comercial ou Aviação Geral)
        peso_max_decolagem    = flight_data["peso_max_decolagem"],                          # Peso máximo de decolagem da aeronave em kg
        velocidade_cruzeiro   = shared["block_speed_kts"],      # Velocidade de cruzeiro da aeronave em nós (knots)
        num_motores           = shared["num_motores"],          # Número de motores na aeronave
        tipo_motor            = flight_data["tipo_motor"],                      # Tipo do motor da aeronave ("turbine" ou "reciprocating")
        preco_aeronave        = shared["preco_aeronave"],       # Preço de mercado da aeronave em USD
        bloco_horas           = shared["block_time_hr"],        # Tempo de bloco da aeronave em horas
        num_pilotos           = flight_data["num_pilotos"],                              # Número de pilotos
        num_copilotos         = flight_data["num_copilotos"],                              # Número de copilotos
        num_eng_voo           = flight_data["num_eng_voo"],                              # Número de engenheiros de voo
        num_comissarios       = flight_data["num_comissarios"],                              # Número de comissários de bordo
        salario_piloto_iniciante      = flight_data["salario_piloto_iniciante"],            # Salário anual de um piloto iniciante (USD/ano)
        salario_copiloto_iniciante    = flight_data["salario_copiloto_iniciante"],             # Salário anual de um copiloto iniciante (USD/ano)
        salario_eng_voo_iniciante     = flight_data["salario_eng_voo_iniciante"],                      # Salário anual de um comissário de bordo iniciante (USD/ano)
        salario_comissario_iniciante  = flight_data["salario_comissario_iniciante"],                      # Tipo da aeronave (Comercial ou Aviação Geral)
        senioridade_piloto            = flight_data["senioridade_piloto"],               # Senioridade do piloto (iniciante, pleno, sênior)
        senioridade_copiloto          = flight_data["senioridade_copiloto"],               # Senioridade do copiloto (iniciante, pleno, sênior)
        senioridade_eng_voo           = flight_data["senioridade_eng_voo"],               # Senioridade do engenheiro de voo (iniciante, pleno, sênior)
        senioridade_comissario        = flight_data["senioridade_comissario"],              # Senioridade do comissário (iniciante, pleno, sênior)
        despesas_viagem_piloto        = flight_data["despesas_viagem_piloto"],                       # Despesas de viagem por piloto (USD/hora de bloco)   - pernoite Caravan Conecta mínimo
        despesas_viagem_copiloto      = flight_data["despesas_viagem_copiloto"],                       # Despesas de viagem por copiloto (USD/hora de bloco) - pernoite Caravan Conecta mínimo
        despesas_viagem_eng_voo       = flight_data["despesas_viagem_eng_voo"],                       # Despesas de viagem por engenheiro de voo (USD/hora de bloco) - pernoite Caravan Conecta mínimo
        despesas_viagem_comissario    = flight_data["despesas_viagem_comissario"],                       # Despesas de viagem por comissário (USD/hora de bloco) - pernoite Caravan Conecta mínimo
        horas_voo_anuais              = shared["annual_hours"], # Número total de horas de voo anuais para toda a tripulação
        combustivel_usado             = flight_data["combustivel_usado"],                   # Quantidade de combustível usado na missão (lbs) - 150 NM : 560 lbs / 770.8 NM : 254  lbs / 500 NM : 1298  lbs
        preco_combustivel             = flight_data["preco_combustivel"],                    # Preço do combustível em USD/galão  - preço de mercado atual
        densidade_combustivel         = flight_data["densidade_combustivel"],                    # Densidade do combustível em lbs/galão
        preco_oleo                    = flight_data["preco_oleo"],                      # Preço do óleo e lubrificantes em USD/galão  - Óleo AeroShell 560,
        densidade_oleo                = flight_data["densidade_oleo"],                    # Densidade do óleo em lbs/galão
        taxa_seguro                   = flight_data["taxa_seguro"],                   # Taxa  de seguro baseado em percentagem do valor de aquisição da aeronave - valor  2.5 % por ser monomotor [Ian]
    )

# --- dicionário principal -------------------------------------------------
inputs = {
    "shared": shared,

    "flight": flight,


    "maint": dict(
        block_time_hr  = shared["block_time_hr"],
        hr_check_a = 1,          # A — Daily check / pré-voo
        hr_check_b = 10,         # B — 25 h
        hr_check_c = 20,         # C — 50 h
        hr_check_d = 40,         # D — 100 h
        hr_check_e = 50,         # E — 200 h
        hr_check_f = 55,         # F — 600 h (ou anual)
        hr_check_i = 0,          # I — inspeções especiais
        # horas de manutenção por tipo de check (motores)
        hr_check_g = 100,        # G — Hot Section Inspection (HSI)
        hr_check_h = 200,        # H — Overhaul de Motor (TBO)
        # demais parâmetros de custo 
        R1_ap      = 8.7,        #  Taxa de mão de obra de manutenção do airframe e sistemas em USD/hora. [planilha sindicato/mercado]
        V_bl       = shared["block_speed_kts"],
        Ne         = shared["num_motores"],
        R1_eng     = 8.7,        #  Taxa de mão de obra de manutenção dos motores em USD/hora. [planilha sindicato/mercado]
        C_mat_apblhr  = 8.7*4,      #  Custo dos materiais de manutenção do airframe e sistemas por bloco de hora em USD/hora.[Ian - 80% insumos 20% mão-de-obra]
        C_mat_engblhr = 8.7*4,      #  Custo dos materiais de manutenção dos motores por bloco de hora em USD/hora. [Ian - 80% insumos 20% mão-de-obra]
        
        f_amb_lab  = 1.25,       #  Fator de sobrecarga para mão de obra.        
       # A mão de obra direta (salário + encargos trabalhistas já embutidos na “man-hour rate”) não paga todo o ecossistema que permite executar o trabalho. 
       # O fator de sobrecarga repassa esse overhead às horas faturadas.
    
       # • Supervisão de manutenção
       # • Ferramentas e equipamentos de apoio (GPU, escadas, hidráulicos)
       # • Energia, água, ar-condicionado do hangar
       # • Administração da oficina, planejamento, qualidade
       # • Seguro de responsabilidade de manutenção
        
        f_amb_mat  = 1.15,      #  Fator de sobrecarga para materiais.   
        
       # Peças compradas pelo preço “na caixa” precisam chegar, ser armazenadas, testadas, 
       # giradas em estoque; esses custos indiretos são capturados pelo multiplicador.      
       # • Frete e seguro de peças
       # • Taxa de importação/desembaraço
       # • Custos de estocagem (almoxarifado, controle de validade)
       # • Ferramentas de inspeção, embalagens especiais
       # • Perdas e sucatas
        
        
    ),
    
    

    "capital": dict(
        price_usd         = shared["preco_aeronave"],
        residual_fraction = 0.12,
        economic_life_yr  = 15,
        annual_hours      = shared["annual_hours"],
        block_speed_kts   = shared["block_speed_kts"],
        scenario          = "own",  # "loan", "lease" ou "own"
        loan_pct          = 0.8,  # Fraction of price financed                            [proporção financiada]  
        loan_interest     = 0.06, # Nominal annual interest rate (decimal)                [ taxa de juros]
        loan_term_yr      = 10,   # Loan amortisation period (years)                      [prazo]
        lease_rate_factor_monthly = 0.015, # Monthly LRF (decimal of price)  [LRF mensal] Jato 0.9%/ monomotor turbo-hélice 1.5 % por ser mais baixo o valor [Ian]
        wacc_equity       = 0.08,        # Opportunity cost of capital (decimal)          [custo de oportunidade indicado[]
    ),

      


    "depr": dict(
        F_dap = 0.70,                           # O caravan tem bom valor de venda depois de 10 anos/ Assim não uso valor do roskna de 85%, mas sim 70% [Ian]
        AEP = shared["preco_aeronave"], 
        Ne = shared["num_motores"],
        EP = 0.25 * shared["preco_aeronave"],   # Preço de um motor (USD)
        Np = 1, 
        PP = 0.02 * shared["preco_aeronave"],   # Preço de uma hélice (USD)  
        ASP = 0.10 * shared["preco_aeronave"],  # Preço dos sistemas aviônicos (USD) 
        DP_ap = 10,                             # Período de depreciação do airframe (anos)
        U_annbl = shared["annual_hours"],
        V_bl    = shared["block_speed_kts"],
        F_deng  = 0.70,                         # Fator de depreciação dos motores # O caravan tem bom valor de venda depois de 10 anos/ Assim não uso valor do roskna de 85%, mas sim 70% [Ian]
        DP_eng = 7,                             # Período de depreciação dos motores (anos)  
        F_dprp  = 0.70,                         # Fator de depreciação das hélices     # O caravan tem bom valor de venda depois de 10 anos/ Assim não uso valor do roskna de 85%, mas sim 70% [Ian]      
        DP_prp = 7,                             # Período de depreciação das hélices (anos) # O caravan tem bom valor de venda depois de 10 anos/ Assim não uso valor do roskna de 85%, mas sim 70% [Ian]
        F_dav = 1.00,                           # Fator de depreciação dos aviônicos
        DP_av = 5,                              # Período de depreciação dos aviônicos (anos)  
        F_dapsp = 0.70,                         # Fator de depreciação das peças sobressalentes da aeronave # O caravan tem bom valor de venda depois de 10 anos/ Assim não uso valor do roskna de 85%, mas sim 70% [Ian]
        F_apsp = 0.10,                          # Fator de peças sobressalentes da aeronave   (ROSKAM)
        DP_apsp = 10,                           # Período de depreciação das peças sobressalentes da aeronave
        F_dengsp = 0.70,                        # Fator de depreciação das peças sobressalentes dos motores # O caravan tem bom valor de venda depois de 10 anos/ Assim não uso valor do roskna de 85%, mas sim 70% [Ian]
        F_engsp = 0.50,                         # Fator de peças sobressalentes dos motores  0.50 (ROSKAM)
        ESPPF = 1.50,                           # Fator de preço das peças sobressalentes dos motores   1.50 (ROSKAM)
        DP_engsp = 7,                           # Período de depreciação das peças sobressalentes dos motores (anos)
    ),




    "taxes": dict(
        mtow_t        = 4.0,
        distance_km   = shared["distance_km"],
        group_type    = "I",
        airport_class = "B",
        tan_unit      = 1.14,
        tat_app_unit  = 126.16,
        tat_adr_unit  = 504.65,
        num_ops       = 1,
    ),
}
