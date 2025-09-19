# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 09:16:21 2025

@author: ITA
"""

# Cálculo do Custo de Depreciação baseado na metodologia de Roskam
# Autor: Adson Agrico de Paula
# Instituição: ITA (Instituto Tecnológico de Aeronáutica)
# Data: [INSERIR DATA ATUAL]

class CustoDepreciacao:
    def __init__(self, F_dap, AEP, Ne, EP, Np, PP, ASP, DP_ap, U_annbl, V_bl, 
                 F_deng, DP_eng, F_dprp, DP_prp, F_dav, DP_av, F_dapsp, F_apsp, DP_apsp, 
                 F_dengsp, F_engsp, ESPPF, DP_engsp):
        """
        Inicializa os parâmetros necessários para o cálculo do custo de depreciação.
        """
        self.F_dap = F_dap  # Fator de depreciação do airframe       0.85
        self.AEP = AEP  # Preço estimado da aeronave (USD)           3000000
        self.Ne = Ne  # Número de motores por aeronave               1
        self.EP = EP  # Preço de um motor (USD)                      0.25 *3000000
        self.Np = Np  # Número de hélices por aeronave               1
        self.PP = PP  # Preço de uma hélice (USD)                    0.02 *3000000  
        self.ASP = ASP  # Preço dos sistemas aviônicos (USD)         0.10 *3000000
        self.DP_ap = DP_ap  # Período de depreciação do airframe (anos)   10 anos 
        self.U_annbl = U_annbl  # Utilização anual em horas de bloco     750 horas 
        self.V_bl = V_bl  # Velocidade de bloco (nm/h)                   132 knots
        self.F_deng = F_deng  # Fator de depreciação dos motores     0.85
        self.DP_eng = DP_eng  # Período de depreciação dos motores (anos)  7 anos
        self.F_dprp = F_dprp  # Fator de depreciação das hélices           0.85
        self.DP_prp = DP_prp  # Período de depreciação das hélices (anos)  7 anos
        self.F_dav = F_dav  # Fator de depreciação dos aviônicos           1
        self.DP_av = DP_av  # Período de depreciação dos aviônicos (anos)  5 anos 
        self.F_dapsp = F_dapsp  # Fator de depreciação das peças sobressalentes da aeronave 0.85
        self.F_apsp = F_apsp  # Fator de peças sobressalentes da aeronave  0.10 (ROSKAM)
        self.DP_apsp = DP_apsp  # Período de depreciação das peças sobressalentes da aeronave (anos)  15 
        self.F_dengsp = F_dengsp  # Fator de depreciação das peças sobressalentes dos motores     0.85
        self.F_engsp = F_engsp  # Fator de peças sobressalentes dos motores  0.50 (ROSKAM)
        self.ESPPF = ESPPF  # Fator de preço das peças sobressalentes dos motores   1.50 (ROSKAM)
        self.DP_engsp = DP_engsp  # Período de depreciação das peças sobressalentes dos motores (anos) 7 anos

    def calcular_custo_total_depreciacao(self):
        """
        Cálculo do custo total de depreciação baseado na metodologia de Roskam.
        """
        
        # Cálculo da depreciação do airframe sem motores, hélices e aviônicos
        
        # C_dap = (F_dap * ((AEP - (Ne * EP) - (Np * PP) - ASP)) / (DP_ap * U_annbl * V_bl))
        # Onde:
        #   - F_dap: Fator de depreciação do airframe
        #   - AEP: Preço estimado da aeronave (USD)
        #   - Ne, EP: Número e preço dos motores
        #   - Np, PP: Número e preço das hélices
        #   - ASP: Preço dos aviônicos
        #   - DP_ap: Período de depreciação do airframe
        
        C_dap = (self.F_dap * ((self.AEP - (self.Ne * self.EP) - (self.Np * self.PP) - self.ASP)) / (self.DP_ap * self.U_annbl * self.V_bl))
        
        # Cálculo da depreciação dos motores
        
        # C_deng = (F_deng * Ne * EP) / (DP_eng * U_annbl * V_bl)
        
        C_deng = (self.F_deng * self.Ne * self.EP) / (self.DP_eng * self.U_annbl * self.V_bl)
        
        # Cálculo da depreciação das hélices
        
        # C_dprp = (F_dprp * Np * PP) / (DP_prp * U_annbl * V_bl)
        
        C_dprp = (self.F_dprp * self.Np * self.PP) / (self.DP_prp * self.U_annbl * self.V_bl)
        
        # Cálculo da depreciação dos aviônicos
        
        # C_dav = (F_dav * ASP) / (DP_av * U_annbl * V_bl)
        
        C_dav = (self.F_dav * self.ASP) / (self.DP_av * self.U_annbl * self.V_bl)
        
        # Cálculo da depreciação das peças sobressalentes do airframe
        
        # C_dapsp = (F_dapsp * F_apsp * (AEP - (Ne * EP))) / (DP_apsp * U_annbl * V_bl)
        
        C_dapsp = (self.F_dapsp * self.F_apsp * (self.AEP - (self.Ne * self.EP))) / (self.DP_apsp * self.U_annbl * self.V_bl)
        
        # Cálculo da depreciação das peças sobressalentes dos motores
        
        # C_dengsp = (F_dengsp * F_engsp * Ne * EP * ESPPF) / (DP_engsp * U_annbl * V_bl)
        
        C_dengsp = (self.F_dengsp * self.F_engsp * self.Ne * self.EP * self.ESPPF) / (self.DP_engsp * self.U_annbl * self.V_bl)
        
        return C_dap + C_deng + C_dprp + C_dav + C_dapsp + C_dengsp
    
    

# Calculo de depreciação para o Caravan 



