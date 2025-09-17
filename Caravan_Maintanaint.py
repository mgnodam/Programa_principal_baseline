# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 08:49:13 2025

@author: ITA
"""

# Cálculo do Custo de Manutenção baseado na metodologia de Roskam
# Autor: Adson Agrico de Paula
# Instituição: ITA (Instituto Tecnológico de Aeronáutica)
# Data: [INSERIR DATA ATUAL]

class CustoManutencao:
    def __init__(self,
                 # horas de manutenção por tipo de check (airframe)
                 block_time_hr, 
                 hr_check_a,      # A — Daily check / pré-voo
                 hr_check_b,      # B — 25 h
                 hr_check_c,      # C — 50 h
                 hr_check_d,      # D — 100 h
                 hr_check_e,      # E — 200 h
                 hr_check_f,      # F — 600 h (ou anual)
                 hr_check_i,      # I — inspeções especiais
                 # horas de manutenção por tipo de check (motores)
                 hr_check_g,      # G — Hot Section Inspection (HSI)
                 hr_check_h,      # H — Overhaul de Motor (TBO)
                 # demais parâmetros de custo 
                 R1_ap,           # Taxa de mão de obra de manutenção do airframe e sistemas em USD/hora.
                 V_bl,            # Velocidade de bloco em nós.
                 Ne,              # Número de motores por aeronave
                 R1_eng,          # Taxa de mão de obra de manutenção dos motores em USD/hora.
                 C_mat_apblhr,    #  Custo dos materiais de manutenção do airframe e sistemas por bloco de hora em USD/hora.
                 C_mat_engblhr,   #  Custo dos materiais de manutenção dos motores por bloco de hora em USD/hora.
                 f_amb_lab,       #   Fator de sobrecarga para mão de obra.
                 f_amb_mat        #  Fator de sobrecarga para materiais.
                 ):    
        

 # ---------------------------------------------------------------
        # 1. INTERVALOS de cada inspeção  (horas de voo) – altere se necessário
 
        int_a = block_time_hr          # A: cada voo
        int_b = 25
        int_c = 50
        int_d = 100
        int_e = 200
        int_f = 600
        int_i = 0.1                    # I: eventual / desprezível
        int_g = 2000                    # G – HSI (exemplo)
        int_h = 4000                   # H – Overhaul (exemplo)
        # ---------------------------------------------------------------

        # 2. >>> horas-homem POR HORA-BLOCO (airframe) <<<
        self.MHR_map_bl = (
            hr_check_a / int_a +
            hr_check_b / int_b +
            hr_check_c / int_c +
            hr_check_d / int_d +
            hr_check_e / int_e +
            hr_check_f / int_f +
            hr_check_i / int_i
        ) / block_time_hr

        # 3. >>> horas-homem POR HORA-BLOCO (motores) <<<
        self.MHR_meng_bl = (
            hr_check_g / int_g +
            hr_check_h / int_h
        ) / block_time_hr

        # 4. Demais atributos – inalterados
        self.R1_ap  = R1_ap
        self.V_bl   = V_bl
        self.Ne     = Ne
        self.R1_eng = R1_eng
        self.C_mat_apblhr  = C_mat_apblhr
        self.C_mat_engblhr = C_mat_engblhr
        self.f_amb_lab = f_amb_lab
        self.f_amb_mat = f_amb_mat
     
     
     
        

    def calcular_custo_total_manutencao(self):
        """
        Cálculo do custo total de manutenção baseado na metodologia de Roskam.
        
        Equação geral:
        DOC_maint = C_lab/ap + C_lab/eng + C_mat/ap + C_mat/eng + C_amb
        
        Onde:
        - C_lab/ap: Custo da mão de obra de manutenção do airframe e sistemas (exceto motores), expresso em USD/nm.
        - C_lab/eng: Custo da mão de obra de manutenção dos motores, expresso em USD/nm.
        - C_mat/ap: Custo dos materiais de manutenção do airframe e sistemas (exceto motores), expresso em USD/nm.
        - C_mat/eng: Custo dos materiais de manutenção dos motores, expresso em USD/nm.
        - C_amb: Custo da sobrecarga aplicada à manutenção, expresso em USD/nm.
        """
                     
        
        """ 
        Equação:
        C_lab/ap = 1.03 * (MHR_map_bl * R1_ap) / V_bl
        
        Explicação:
        - O fator 1.03 representa um ajuste para cobrir custos extras decorrentes de atrasos operacionais e manutenções não programadas.
        - MHR_map_bl é o número de horas de mão de obra de manutenção do airframe e sistemas por bloco de hora.
        - R1_ap é a taxa de mão de obra por hora.
        - V_bl é a velocidade de bloco, convertendo o custo para USD por milha náutica.
        """
        
        C_lab_ap = 1.03 * (self.MHR_map_bl * self.R1_ap) / self.V_bl
        
        """ 
        Equação:
        C_lab/eng = 1.03 * 1.3 * Ne * (MHR_meng_bl * R1_eng) / V_bl
    
        Explicação:
        - O fator 1.03 ajusta para custos adicionais não planejados, similar ao custo do airframe.
        - O fator 1.3 reflete o impacto de manutenções dependentes do ciclo de operação dos motores, como trocas de componentes cíclicos.
        - Ne é o número de motores na aeronave.
        - MHR_meng_bl é o número de horas de mão de obra necessárias para manutenção dos motores por bloco de hora.
        - R1_eng é a taxa de mão de obra para manutenção dos motores.
        """
                
        C_lab_eng = 1.03 * 1.3 * self.Ne * (self.MHR_meng_bl * self.R1_eng) / self.V_bl
        
        
        """ 
        Equação:
        C_mat/ap = 1.03 * (C_mat/apblhr) / V_bl
        
        Explicação:
        - O fator 1.03 cobre custos adicionais imprevistos na manutenção de materiais.
        - C_mat/apblhr é o custo de materiais de manutenção do airframe e sistemas por bloco de hora.
        - V_bl converte o custo para USD por milha náutica.
        """
        
        C_mat_ap = 1.03 * self.C_mat_apblhr / self.V_bl
        
        
        """ 
        Equação:
        C_mat/eng = 1.03 * 1.3 * Ne * (C_mat/engblhr) / V_bl
        
        Explicação:
        - O fator 1.03 cobre custos adicionais não planejados.
        - O fator 1.3 reflete o custo adicional para peças e materiais dependentes do ciclo operacional dos motores.
        - Ne é o número de motores na aeronave.
        - C_mat/engblhr é o custo dos materiais de manutenção dos motores por bloco de hora.
        """
        
        C_mat_eng = 1.03 * 1.3 * self.Ne * self.C_mat_engblhr / self.V_bl
        
        
        """ 
        Equação:
        C_amb = 1.03 * [(f_amb/lab * (C_lab/ap + C_lab/eng)) + (f_amb/mat * (C_mat/ap + C_mat/eng))] / V_bl
        
        Explicação:
        - f_amb_lab e f_amb_mat são fatores de sobrecarga para mão de obra e materiais, cobrindo custos indiretos como administração e infraestrutura.
        - Os termos C_lab/ap e C_lab/eng referem-se aos custos de mão de obra para manutenção do airframe e motores.
        - Os termos C_mat/ap e C_mat/eng referem-se aos custos de materiais para manutenção do airframe e motores.
        """
        
        
        C_amb = 1.03 * ((self.f_amb_lab * (C_lab_ap + C_lab_eng)) + (self.f_amb_mat * (C_mat_ap + C_mat_eng))) / self.V_bl
        
        
        return C_lab_ap + C_lab_eng + C_mat_ap + C_mat_eng + C_amb