# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 17:29:26 2025

@author: ITA
"""

# ---------------------------------------------------------------------------
#  Caravan_DOC_main.py
# ---------------------------------------------------------------------------
"""
Fluxo:
  1. Lê dicionário de inputs.
  2. Chama cada módulo de custo:
       - Flight (tripulação + combustível + seguro)
       - Manutenção
       - Depreciação
       - Custo do dinheiro (capital)
       - Taxas de navegação
  3. Converte tudo para USD/nm; soma DOC_total.
  4. Salva resultados em “Caravan_DOC.dat”.
  5. Gera gráfico de barras com Matplotlib.
"""
import json
from pathlib import Path
import matplotlib.pyplot as plt

from Operation_input_Caravan import inputs

# ---- módulos de cálculo fornecidos pelo usuário --------------------------
from Caravan_Flight import Aeronave
from Caravan_Maintanaint import CustoManutencao
from Caravan_Depreciation import CustoDepreciacao
from Caravan_Capital_cost import CapitalCostInputs, compute_capital_cost
from Caravan_Taxes import nav_charges     # já devolve USD/nm se usd_per_brl != None

# -------- 1. FLIGHT (tripulação + fuel + oil + insurance) ------------------
air = Aeronave(**inputs["flight"])
air.calcular_custo_tripulacao()
air.calcular_custo_combustivel_oleo()
air.calcular_custo_seguro()
c_flight      = air.calcular_doc()                   # USD/nm

# -------- 2. MANUTENÇÃO ----------------------------------------------------
maint_params  = inputs["maint"]
c_maint       = CustoManutencao(**maint_params).calcular_custo_total_manutencao()  # USD/nm

# -------- 3. DEPRECIAÇÃO ---------------------------------------------------
depr_params   = inputs["depr"]
c_depr        = CustoDepreciacao(**depr_params).calcular_custo_total_depreciacao() # USD/nm

# -------- 4. CAPITAL / CUSTO DO DINHEIRO -----------------------------------
cap_inp_dict  = inputs["capital"]
scenario      = cap_inp_dict.pop("scenario")
cap_inputs    = CapitalCostInputs(**cap_inp_dict)
c_capital     = compute_capital_cost(cap_inputs, scenario).cost_per_nm_usd        # USD/nm

# -------- 5. TAXAS (DECEA) -------------------------------------------------
tax_params    = inputs["taxes"] | {"usd_per_brl": inputs["usd_per_brl"]}
c_taxes       = nav_charges(**tax_params).usd_per_nm                              # USD/nm

# -------- 6. DOC TOTAL -----------------------------------------------------
components = {
    "Tripulação + Combustível + Seguro": c_flight,
    "Manutenção"        : c_maint,
    "Depreciação"       : c_depr,
    "Custo do Dinheiro" : c_capital,
    "Taxas"             : c_taxes,
}
doc_total = sum(components.values())

# -------- 7. Salva arquivo .dat -------------------------------------------
out_path = Path("Caravan_DOC.dat")
with out_path.open("w", encoding="utf-8") as f:
    for k, v in components.items():
        f.write(f"{k:35s} {v:10.4f} USD/nm\n")
    f.write(f"\nTOTAL DOC                     {doc_total:10.4f} USD/nm\n")
print(f"Resultados gravados em {out_path.resolve()}")

# -------- 8. Gráfico de barras --------------------------------------------
plt.figure(figsize=(8,4))
plt.bar(components.keys(), components.values())
plt.ylabel("USD / milha náutica")
plt.title("DOC – Cessna 208B Caravan (Azul Conecta)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("Caravan_DOC_bars.png", dpi=300)
plt.show()