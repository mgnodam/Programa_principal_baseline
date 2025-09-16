# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 17:07:14 2025

@author: ITA
"""

# ---------------------------------------------------------------------------
#  car an_inputs.py
# ---------------------------------------------------------------------------
#  Todos os dados necessários para os cálculos em UM só dicionário.
#  Basta atualizar aqui (ou carregar de JSON/CSV, se preferir).

inputs = {
    # --- parâmetros operacionais básicos ----------------------------------
    "annual_hours"    : 750,        # block-hours/ano
    "block_time_hr"   : 2.0,        # h
    "block_speed_kts" : 132,        # ≈ V_bl
    "distance_km"     : 350,        # km (média na FIR p/ cálculo de taxas)
    "usd_per_brl"     : 0.20,       # câmbio para Roskam (1 R$ = 0,20 USD)
    "preco_aeronave"  : 3_000_000,  # Preço da aeronave

    # --- aeronave & tripulação (Caravan_Flight) ---------------------------
    "flight" : dict(
        tipo                  = "Aviação Geral",
        peso_max_decolagem    = 3_995,
        velocidade_cruzeiro   = 132,
        num_motores           = 1,
        tipo_motor            = "turbine",
        preco_aeronave        = 3000000,
        bloco_horas           = 2.0,
        num_pilotos           = 1,
        num_copilotos         = 0,
        num_eng_voo           = 0,
        num_comissarios       = 0,
        salario_piloto_iniciante      = 23_415,
        salario_copiloto_iniciante    = 0,
        salario_eng_voo_iniciante     = 0,
        salario_comissario_iniciante  = 0,
        senioridade_piloto            = "iniciante",
        senioridade_copiloto          = "iniciante",
        senioridade_eng_voo           = "iniciante",
        senioridade_comissario        = "iniciante",
        despesas_viagem_piloto        = 45,
        despesas_viagem_copiloto      = 0,
        despesas_viagem_eng_voo       = 0,
        despesas_viagem_comissario    = 0,
        horas_voo_anuais              = 750,
        combustivel_usado             = 772,     # lb por voo
        preco_combustivel             = 2.00,    # USD/gal
        densidade_combustivel         = 6.74,    # lb/gal
        preco_oleo                    = 134,     # USD/gal
        densidade_oleo                = 8.33,    # lb/gal
        taxa_seguro                   = 0.015,   # 1,5 % do hull
    ),

    # --- manutenção (Caravan_Maintanaint) ---------------------------------
    "maint" : dict(
        block_time_hr = 2, hr_check_a = 1,  hr_check_b = 10,  hr_check_c = 20,
        hr_check_d = 40,  hr_check_e =50,  hr_check_f =55,
        hr_check_i = 0,
        hr_check_g =100,  hr_check_h =200,
        R1_ap      = 50,
        V_bl       = 132,
        Ne         = 1,
        R1_eng     = 50,
        C_mat_apblhr = 50,
        C_mat_engblhr= 50,
        f_amb_lab  = 1.25,
        f_amb_mat  = 1.15,
    ),

    # --- capital e custo do dinheiro (Caravan_Capital_cost) ---------------
    "capital" : dict(
        price_usd         = 3_000_000,
        residual_fraction = 0.12,
        economic_life_yr  = 15,
        annual_hours      = 750,
        block_speed_kts   = 132,
        scenario          = "own",   # "loan", "lease" ou "own"
        loan_pct          = 0.8,     loan_interest = 0.06, loan_term_yr = 10,
        lease_rate_factor_monthly = 0.009,
        wacc_equity       = 0.08,
    ),

    # --- depreciação (Caravan_Depreciation) -------------------------------
    "depr" : dict(
        F_dap=0.85, AEP=2_000_000, Ne=1, EP=0.25*2_000_000,
        Np=1, PP=0.02*2_000_000, ASP=0.10*2_000_000, DP_ap=10,
        U_annbl=750, V_bl=132, F_deng=0.85, DP_eng=7,
        F_dprp=0.85, DP_prp=7, F_dav=1.00, DP_av=5,
        F_dapsp=0.85, F_apsp=0.10, DP_apsp=10,
        F_dengsp=0.85, F_engsp=0.50, ESPPF=1.50, DP_engsp=7,
    ),

    # --- taxas de navegação (Caravan_Taxes) -------------------------------
    "taxes" : dict(
        mtow_t        = 4.0,
        distance_km   = 350.0,
        group_type    = "I",
        airport_class = "B",
        tan_unit      = 1.14,
        tat_app_unit  = 126.16,
        tat_adr_unit  = 504.65,
        num_ops       = 1,          # pouso apenas
    ),
}