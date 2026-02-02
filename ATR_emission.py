# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 21:12:13 2025

@author: ITA
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 10:08:09 2025
@author: ITA
"""

import matplotlib.pyplot as plt
import pandas as pd

from ATR_Operation_input_ian import inputs

# ---- módulos de cálculo fornecidos pelo usuário --------------------------
from ATR_Flight import Aeronave
from ATR_Maintanaint import CustoManutencao
from ATR_Depreciation import CustoDepreciacao
from ATR_Capital_cost import CapitalCostInputs, compute_capital_cost
from ATR_tax import TaxasNavegacao     # já devolve USD/nm se usd_per_brl != None

# =========================
# ENTRADAS DO PROGRAMA
# =========================

block_time_hr =  1.9  # 250 nm @ 132 knots híbrido 350 kW
annual_hours = 800
missions = annual_hours/block_time_hr

inputs = {


    "fuel_jetA1_only_kg": missions*590.1,

    "fuel_jetA1_hybrid_solar_kg": missions*509.6,
    "electric_energy_solar_kwh": missions*7.9,

    "fuel_jetA1_hybrid_hydro_kg": missions*509.6,
    "electric_energy_hydro_kwh": missions*7.9,

    "emission_factors": {
        "Jet-A1": {"WTT": 0.014, "TTW": 0.0738, "WTW": 0.0878},
        "SAF": {"WTT": 0.024, "TTW": 0.00, "WTW": 0.024},
        "Hydro": {"WTT": 0.012, "TTW": 0.00, "WTW": 0.012},
        "Solar": {"WTT": 0.011, "TTW": 0.00, "WTW": 0.011}
    },

    "conversion_efficiency": {
        "Jet-A1": 0.30,
        "SAF": 0.30,
        "Hydro": 0.75,
        "Solar": 0.75
    },

    "LHV_JetA1": 43.0  # MJ/kg
}

# =========================
# CÁLCULO DE EMISSÕES
# =========================
def calculate_emissions():
    results = {}
    eff_jet = inputs["conversion_efficiency"]["Jet-A1"]

    # Jet-A1
    energy_jet_only = (inputs["fuel_jetA1_only_kg"] * inputs["LHV_JetA1"]) / eff_jet
    emissions_jet = {
        stage: energy_jet_only * ef
        for stage, ef in inputs["emission_factors"]["Jet-A1"].items()
    }
    results["Jet-A1"] = emissions_jet

    # SAF
    energy_saf = energy_jet_only
    emissions_saf = {
        stage: energy_saf * ef
        for stage, ef in inputs["emission_factors"]["SAF"].items()
    }
    results["SAF"] = emissions_saf

    # Hybrid Solar
    energy_jet_hybrid_solar = (inputs["fuel_jetA1_hybrid_solar_kg"] * inputs["LHV_JetA1"]) / eff_jet
    energy_solar = (inputs["electric_energy_solar_kwh"] * 3.6) / inputs["conversion_efficiency"]["Solar"]

    emissions_jet_solar = {
        stage: energy_jet_hybrid_solar * ef
        for stage, ef in inputs["emission_factors"]["Jet-A1"].items()
    }
    emissions_solar = {
        stage: energy_solar * ef
        for stage, ef in inputs["emission_factors"]["Solar"].items()
    }
    results["Hybrid Solar"] = {
        stage: emissions_jet_solar[stage] + emissions_solar[stage]
        for stage in emissions_jet_solar
    }

    # Hybrid Hydro
    energy_jet_hybrid_hydro = (inputs["fuel_jetA1_hybrid_hydro_kg"] * inputs["LHV_JetA1"]) / eff_jet
    energy_hydro = (inputs["electric_energy_hydro_kwh"] * 3.6) / inputs["conversion_efficiency"]["Hydro"]

    emissions_jet_hydro = {
        stage: energy_jet_hybrid_hydro * ef
        for stage, ef in inputs["emission_factors"]["Jet-A1"].items()
    }
    emissions_hydro = {
        stage: energy_hydro * ef
        for stage, ef in inputs["emission_factors"]["Hydro"].items()
    }
    results["Hybrid Hydro"] = {
        stage: emissions_jet_hydro[stage] + emissions_hydro[stage]
        for stage in emissions_jet_hydro
    }
    
    return results

# =========================
# EXECUÇÃO DOS CÁLCULOS
# =========================
emission_data = calculate_emissions()
df = pd.DataFrame(emission_data).T
df.index.name = "Configuration"

# =========================
# SALVAR EM ARQUIVO .dat
# =========================
df.to_csv("emissions_summary_configurations.dat", sep='\t')

# =========================
# PLOTTING AND SAVING GRAPH
# =========================
def plot_emissions(df, filename="annual_emissions_by_configuration.png"):
    df.plot(kind="bar", figsize=(12, 6))
    plt.title("Annual Emissions (kg CO₂) by Propulsion Configuration", fontsize=16)
    plt.ylabel("Emissions (kg CO₂)", fontsize=14)
    plt.xlabel("Configuration", fontsize=14)
    plt.xticks(rotation=0, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()

# Executar a plotagem e salvar o gráfico
plot_emissions(df)