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
    annual_hours     = 750,
    block_time_hr    = 2.0,
    block_speed_kts  = 132,
    distance_km      = 350,
    usd_per_brl      = 0.20,
    preco_aeronave   = 2_300_000,
    num_motores      = 1,
)

# --- dicionário principal -------------------------------------------------
inputs = {
    "shared": shared,

    "flight": dict(
        tipo                  = "Aviação Geral",
        peso_max_decolagem    = 3_995,
        velocidade_cruzeiro   = shared["block_speed_kts"],
        num_motores           = shared["num_motores"],
        tipo_motor            = "turbine",
        preco_aeronave        = shared["preco_aeronave"],
        bloco_horas           = shared["block_time_hr"],
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
        horas_voo_anuais              = shared["annual_hours"],
        combustivel_usado             = 772,
        preco_combustivel             = 2.00,
        densidade_combustivel         = 6.74,
        preco_oleo                    = 134,
        densidade_oleo                = 8.33,
        taxa_seguro                   = 0.015,
    ),

    "maint": dict(
        block_time_hr  = shared["block_time_hr"],
        hr_check_a = 1,  hr_check_b = 10,  hr_check_c = 20,
        hr_check_d = 40, hr_check_e = 50, hr_check_f = 55,
        hr_check_i = 0,
        hr_check_g = 100, hr_check_h = 200,
        R1_ap      = 50,
        V_bl       = shared["block_speed_kts"],
        Ne         = shared["num_motores"],
        R1_eng     = 50,
        C_mat_apblhr  = 50,
        C_mat_engblhr = 50,
        f_amb_lab  = 1.25,
        f_amb_mat  = 1.15,
    ),

    "capital": dict(
        price_usd         = shared["preco_aeronave"],
        residual_fraction = 0.12,
        economic_life_yr  = 15,
        annual_hours      = shared["annual_hours"],
        block_speed_kts   = shared["block_speed_kts"],
        scenario          = "own",  # "loan", "lease" ou "own"
        loan_pct          = 0.8,
        loan_interest     = 0.06,
        loan_term_yr      = 10,
        lease_rate_factor_monthly = 0.009,
        wacc_equity       = 0.08,
    ),

    "depr": dict(
        F_dap = 0.85, AEP = 2_000_000, Ne = shared["num_motores"],
        EP = 0.25 * 2_000_000, Np = 1, PP = 0.02 * 2_000_000,
        ASP = 0.10 * 2_000_000, DP_ap = 10,
        U_annbl = shared["annual_hours"],
        V_bl    = shared["block_speed_kts"],
        F_deng  = 0.85, DP_eng = 7,
        F_dprp  = 0.85, DP_prp = 7, F_dav = 1.00, DP_av = 5,
        F_dapsp = 0.85, F_apsp = 0.10, DP_apsp = 10,
        F_dengsp = 0.85, F_engsp = 0.50, ESPPF = 1.50, DP_engsp = 7,
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
