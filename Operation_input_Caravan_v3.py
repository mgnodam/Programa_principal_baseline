# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 11:02:44 2025

@author: ITA
"""

# ---------------------------------------------------------------------------
#  car an_inputs.py
# ---------------------------------------------------------------------------

# --- parâmetros operacionais compartilhados -------------------------------
shared = dict(
    annual_hours     = 800, # Quantidade de horas de bloco que a aeronave voa em um ano de operação. 
                            # Usada como divisor para transformar custos anuais (salários, seguro, capital) em custos por hora ou por milha.
    block_time_hr    = 1.7, # Duração média de um ciclo “bloco-bloco”: do acionamento de calços antes da saída (off-blocks) até 
                            # a recolocação dos calços após o pouso (on-blocks). Inclui taxi, decolagem, subida, cruzeiro, descida, aproximação, 
                            # arremate se ocorrer, taxi de chegada e eventuais esperas.
    block_speed_kts  = 132, # Velocidade média “de bloco”, obtida dividindo a distância bloco (nm) pelo tempo de bloco. Combina cruzeiro mais todas as fases de voo, 
                            # sendo menor do que a velocidade de cruzeiro pura. Necessária para converter custos por hora em custos por milha náutica.
    distance_km      = 350, # Distância geográfica da rota de estudo, medida em quilômetros. Se o modelo usa milhas náuticas internamente, converte-se por 1 nm = 1,852 km.
                            # Serve para estimar consumo e para dividir custos de viagem.
    usd_per_brl      = 0.20,# Taxa de câmbio utilizada para converter custos cotados em reais (BRL) para dólares americanos (USD), unidade tradicional nos estudos DOC de Roskam.
    preco_aeronave   = 2_300_000, # Valor de mercado ou custo de aquisição da aeronave (airframe + motores no estado considerado). 
                                  # Entra no cálculo de depreciação, seguro e custo de capital (juros ou lease).
    num_motores      = 1,  # Número total de motores instalados. Impacta consumo de óleo (motores a turbina), manutenção de grupo moto-propulsor e,
                           # em estudos híbridos, o dimensionamento de geradores e sistemas auxiliares.
)

# --- dicionário principal -------------------------------------------------
inputs = {
    "shared": shared,

    "flight": dict(
        tipo                  = "Aviação Geral",                # Tipo da aeronave (Comercial ou Aviação Geral)
        peso_max_decolagem    = 3_995,                          # Peso máximo de decolagem da aeronave em kg
        velocidade_cruzeiro   = shared["block_speed_kts"],      # Velocidade de cruzeiro da aeronave em nós (knots)
        num_motores           = shared["num_motores"],          # Número de motores na aeronave
        tipo_motor            = "turbine",                      # Tipo do motor da aeronave ("turbine" ou "reciprocating")
        preco_aeronave        = shared["preco_aeronave"],       # Preço de mercado da aeronave em USD
        bloco_horas           = shared["block_time_hr"],        # Tempo de bloco da aeronave em horas
        num_pilotos           = 1,                              # Número de pilotos
        num_copilotos         = 1,                              # Número de copilotos
        num_eng_voo           = 0,                              # Número de engenheiros de voo
        num_comissarios       = 0,                              # Número de comissários de bordo
        salario_piloto_iniciante      = 20205.72391,            # Salário anual de um piloto iniciante (USD/ano)
        salario_copiloto_iniciante    = 17045.6422,             # Salário anual de um copiloto iniciante (USD/ano)
        salario_eng_voo_iniciante     = 0,                      # Salário anual de um comissário de bordo iniciante (USD/ano)
        salario_comissario_iniciante  = 0,                      # Tipo da aeronave (Comercial ou Aviação Geral)
        senioridade_piloto            = "sênior",               # Senioridade do piloto (iniciante, pleno, sênior)
        senioridade_copiloto          = "sênior",               # Senioridade do copiloto (iniciante, pleno, sênior)
        senioridade_eng_voo           = "sênior",               # Senioridade do engenheiro de voo (iniciante, pleno, sênior)
        senioridade_comissario        = "sênior",               # Senioridade do comissário (iniciante, pleno, sênior)
        despesas_viagem_piloto        = 0,                      # Despesas de viagem por piloto (USD/hora de bloco)   - pernoite Caravan Conecta mínimo
        despesas_viagem_copiloto      = 0,                      # Despesas de viagem por copiloto (USD/hora de bloco) - pernoite Caravan Conecta mínimo
        despesas_viagem_eng_voo       = 0,                      # Despesas de viagem por engenheiro de voo (USD/hora de bloco) - pernoite Caravan Conecta mínimo
        despesas_viagem_comissario    = 0,                      # Despesas de viagem por comissário (USD/hora de bloco) - pernoite Caravan Conecta mínimo
        horas_voo_anuais              = shared["annual_hours"], # Número total de horas de voo anuais para toda a tripulação
        combustivel_usado             = 770.8,                  # Quantidade de combustível usado na missão (lbs) - 150 NM : 560 lbs / 770.8 NM : 254  lbs / 500 NM : 1298  lbs
        preco_combustivel             = 3.05,                   # Preço do combustível em USD/galão  - preço de mercado atual
        densidade_combustivel         = 6.74,                   # Densidade do combustível em lbs/galão
        preco_oleo                    = 95,                    # Preço do óleo e lubrificantes em USD/galão  - Óleo AeroShell 560,
        densidade_oleo                = 8.33,                   # Densidade do óleo em lbs/galão
        taxa_seguro                   = 0.013,                  # Taxa  de seguro baseado em percentagem do valor de aquisição da aeronave - valor intermediário
    ),


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
        C_mat_apblhr  = 8.7* 0.30,      #  Custo dos materiais de manutenção do airframe e sistemas por bloco de hora em USD/hora.[documento sobre hora-homem/insumos]
        C_mat_engblhr = 8.7 * 0.40,      #  Custo dos materiais de manutenção dos motores por bloco de hora em USD/hora. [documento sobre hora-homem/insumos]
        
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
        scenario          = "lease",  # "loan", "lease" ou "own"
        loan_pct          = 0.8,  # Fraction of price financed                         [proporção financiada]  
        loan_interest     = 0.06, # Nominal annual interest rate (decimal)       [ taxa de juros]
        loan_term_yr      = 10,   # Loan amortisation period (years)                  [prazo]
        lease_rate_factor_monthly = 0.009, # Monthly LRF (decimal of price)  [LRF mensal]
        wacc_equity       = 0.08,        # Opportunity cost of capital (decimal)          [custo de oportunidade indicado[]
    ),

      


    "depr": dict(
        F_dap = 0.85, 
        AEP = shared["preco_aeronave"], 
        Ne = shared["num_motores"],
        EP = 0.25 * shared["preco_aeronave"],   # Preço de um motor (USD)
        Np = 1, 
        PP = 0.02 * shared["preco_aeronave"],   # Preço de uma hélice (USD)  
        ASP = 0.10 * shared["preco_aeronave"],  # Preço dos sistemas aviônicos (USD) 
        DP_ap = 10,                             # Período de depreciação do airframe (anos)
        U_annbl = shared["annual_hours"],
        V_bl    = shared["block_speed_kts"],
        F_deng  = 0.85,                         # Fator de depreciação dos motores
        DP_eng = 7,                             # Período de depreciação dos motores (anos)  
        F_dprp  = 0.85,                          # Fator de depreciação das hélices           
        DP_prp = 7,                             # Período de depreciação das hélices (anos)
        F_dav = 1.00,                           # Fator de depreciação dos aviônicos
        DP_av = 5,                              # Período de depreciação dos aviônicos (anos)  
        F_dapsp = 0.85,                         # Fator de depreciação das peças sobressalentes da aeronave 
        F_apsp = 0.10,                          # Fator de peças sobressalentes da aeronave   (ROSKAM)
        DP_apsp = 10,                           # Período de depreciação das peças sobressalentes da aeronave
        F_dengsp = 0.85,                        # Fator de depreciação das peças sobressalentes dos motores
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
