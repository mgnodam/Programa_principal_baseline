# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 09:42:57 2025

@author: ITA
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 3 11:04:13 2025
@author: ITA
"""

# Cálculo das Taxas de Navegação Aérea Brasileira (ICA 12-35/2023)

import math

KM_TO_NM = 0.539957  # 1 km = 0.539957 nautical mile

class TaxasNavegacao:
    def __init__(self,
                 mtow_t,         # Peso máximo de decolagem em toneladas
                 distance_km,    # Distância da missão em km
                 group_type,     # Tipo de grupo (I, II, III...)
                 airport_class,  # Classe do aeroporto (A, B, C...)
                 tan_unit,       # Tarifa TAN unitária
                 tat_app_unit,   # Tarifa de aproximação unitária
                 tat_adr_unit,   # Tarifa de aeródromo unitária
                 num_ops,        # Número de operações APP/TWR (1 ou 2)
                 usd_per_brl,    # Câmbio R$ → USD
                 fp_floor=0.50,  # Piso do Fp
                 fp_cap=6.40):   # Teto do Fp

        self.mtow_t        = mtow_t
        self.distance_km   = distance_km
        self.group_type    = group_type
        self.airport_class = airport_class
        self.tan_unit      = tan_unit
        self.tat_app_unit  = tat_app_unit
        self.tat_adr_unit  = tat_adr_unit
        self.num_ops       = num_ops
        self.usd_per_brl   = usd_per_brl
        self.fp_floor      = fp_floor
        self.fp_cap        = fp_cap

        # Cálculo direto ao instanciar
        self.fp          = self.calcular_fp()
        self.tan         = self.tan_unit * self.distance_km * self.fp
        self.tat_app     = self.tat_app_unit * self.fp * self.num_ops
        self.tat_adr     = self.tat_adr_unit * self.fp * self.num_ops
        self.total       = self.tan + self.tat_app + self.tat_adr
        self.usd_per_nm  = self.converter_para_usd_por_nm()

    def calcular_fp(self):
        """Calcula o Fator de Peso (Fp) limitado aos pisos e tetos."""
        bruto = math.sqrt(self.mtow_t / 50.0)
        return max(self.fp_floor, min(bruto, self.fp_cap))

    def converter_para_usd_por_nm(self):
        """Converte o total em reais para USD por milha náutica."""
        distance_nm = self.distance_km * KM_TO_NM
        total_usd = self.total * self.usd_per_brl
        return total_usd / distance_nm