# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 11:04:13 2025

@author: ITA
"""

"""
------------------------------------------------------------------------------
  NavigationCharges.py   (versão estendida: operações múltiplas + USD/NM)
------------------------------------------------------------------------------
  Calcula as tarifas de navegação aérea brasileiras (ICA 12-35/2023):

      • TAN      – Tarifa de Uso das Comunicações e Auxílios em Rota
      • TAT_APP  – Tarifa de Aproximação  (serviço APP)
      • TAT_ADR  – Tarifa de Aeródromo / Torre (serviço TWR)
      • TOTAL    – Soma das três tarifas

  NOVO:
      • num_ops       : quantas vezes APP/TWR são cobrados na perna
                        (1 = só no pouso; 2 = decolagem + pouso)
      • usd_per_brl   : câmbio opcional para converter R$ → USD
      • custo USD/NM  : saída direta para metodologia Roskam

------------------------------------------------------------------------------
"""

import math
from dataclasses import dataclass

# ---------- conversão de unidades ------------------------------------------
KM_TO_NM = 0.539957         # 1 km = 0,539957 nautical mile

@dataclass
class ChargeBreakdown:
    fp: float
    tan: float
    tat_app: float
    tat_adr: float
    total: float
    usd_per_nm: float 


def calc_fp(mtow_t: float,
            fp_floor: float = 0.50,
            fp_cap:   float = 6.40) -> float:
    """Fp = √(MTOW/50) limitado aos pisos/tetos da ICA 12-35."""
    raw_fp = math.sqrt(mtow_t / 50.0)
    return max(fp_floor, min(raw_fp, fp_cap))


def nav_charges(mtow_t: float,
                distance_km: float,
                group_type: str,
                airport_class: str,
                tan_unit: float,
                tat_app_unit: float,
                tat_adr_unit: float,
                num_ops: int = 1,
                usd_per_brl: float,
                fp_floor: float = 0.50,
                fp_cap:   float = 6.40) -> ChargeBreakdown:
    """
    Calcula TAN, TAT_APP, TAT_ADR e custo total.

    • num_ops  → quantas operações APP/TWR incidem na perna (1 ou 2).
    • usd_per_brl → se fornecido, devolve também custo em USD por NM.
    """
    fp = calc_fp(mtow_t, fp_floor, fp_cap)

    tan      = tan_unit     * distance_km * fp
    tat_app  = tat_app_unit * fp * num_ops
    tat_adr  = tat_adr_unit * fp * num_ops
    total_r  = tan + tat_app + tat_adr

    # Converte para USD/NM, se solicitado

   distance_nm = distance_km * KM_TO_NM
   total_usd   = total_r * usd_per_brl
   usd_per_nm  = total_usd / distance_nm

    return ChargeBreakdown(fp, tan, tat_app, tat_adr, total_r, usd_per_nm)


