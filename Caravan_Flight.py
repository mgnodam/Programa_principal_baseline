# -*- coding: utf-8 -*-
"""
 Cálculo do Custo Operacional Direto (DOC) baseado em Roskam
 Autor: Adson Agrico de Paula
 Instituição: ITA (Instituto Tecnológico de Aeronáutica)
 Data: [INSERIR DATA ATUAL]
 Descrição: Este programa calcula o custo operacional direto (DOC) de uma aeronave comercial ou de aviação geral,
           utilizando a metodologia de Roskam. O DOC é expresso em USD por milha náutica (USD/nm) e é dividido nos seguintes componentes:

           DOC = DOC_flt + DOC_maint + DOC_depr +
                 + DOC_lnr + DOC_fin

   Onde:
           DOC_flt   -> Custo direto de voo (tripulação, combustível e seguro)
           DOC_maint -> Custo direto de manutenção (mão de obra e materiais)
           DOC_depr  -> Custo de depreciação
           DOC_lnr   -> Taxas aeroportuárias e de navegação
           DOC_fin   -> Custo de financiamento da aeronave

 O programa permite inserir os dados da aeronave e calcula o DOC com base nas equações apresentadas por Roskam.

"""


class Aeronave:
    def __init__(self, tipo, peso_max_decolagem, velocidade_cruzeiro, num_motores, tipo_motor,
                 preco_aeronave, bloco_horas, num_pilotos, num_copilotos, num_eng_voo, num_comissarios, 
                 salario_piloto_iniciante, salario_copiloto_iniciante, salario_eng_voo_iniciante, salario_comissario_iniciante,
                 senioridade_piloto, senioridade_copiloto, senioridade_eng_voo, senioridade_comissario,
                 despesas_viagem_piloto, despesas_viagem_copiloto, despesas_viagem_eng_voo, despesas_viagem_comissario,
                 horas_voo_anuais, combustivel_usado, preco_combustivel, densidade_combustivel, preco_oleo, densidade_oleo,taxa_seguro):
        
        """
   Inicializa os parâmetros da aeronave.
   :param tipo: Tipo da aeronave (Comercial ou Aviação Geral)
   :param peso_max_decolagem: Peso máximo de decolagem da aeronave em kg
   :param velocidade_cruzeiro: Velocidade de cruzeiro da aeronave em nós (knots)
   :param num_motores: Número de motores na aeronave
   :param tipo_motor: Tipo do motor da aeronave ("turbine" ou "reciprocating")
   :param preco_aeronave: Preço de mercado da aeronave em USD
   :param bloco_horas: Tempo de bloco da aeronave em horas
   :param num_pilotos: Número de pilotos
   :param num_copilotos: Número de copilotos
   :param num_eng_voo: Número de engenheiros de voo
   :param num_comissarios: Número de comissários de bordo
   :param salario_piloto_iniciante: Salário anual de um piloto iniciante (USD/ano)
   :param salario_copiloto_iniciante: Salário anual de um copiloto iniciante (USD/ano)
   :param salario_eng_voo_iniciante: Salário anual de um engenheiro de voo iniciante (USD/ano)
   :param salario_comissario_iniciante: Salário anual de um comissário de bordo iniciante (USD/ano)
   :param senioridade_piloto: Senioridade do piloto (iniciante, pleno, sênior)
   :param senioridade_copiloto: Senioridade do copiloto (iniciante, pleno, sênior)
   :param senioridade_eng_voo: Senioridade do engenheiro de voo (iniciante, pleno, sênior)
   :param senioridade_comissario: Senioridade do comissário (iniciante, pleno, sênior)
   :param despesas_viagem_piloto: Despesas de viagem por piloto (USD/hora de bloco)
   :param despesas_viagem_copiloto: Despesas de viagem por copiloto (USD/hora de bloco)
   :param despesas_viagem_eng_voo: Despesas de viagem por engenheiro de voo (USD/hora de bloco)
   :param despesas_viagem_comissario: Despesas de viagem por comissário (USD/hora de bloco)
   :param horas_voo_anuais: Número total de horas de voo anuais para toda a tripulação
   :param combustivel_usado: Quantidade de combustível usado na missão (lbs)
   :param preco_combustivel: Preço do combustível em USD/galão
   :param densidade_combustivel: Densidade do combustível em lbs/galão
   :param preco_oleo: Preço do óleo e lubrificantes em USD/galão
   :param densidade_oleo: Densidade do óleo em lbs/galão
   
      """


        self.tipo = tipo
        self.peso_max_decolagem = peso_max_decolagem
        self.velocidade_cruzeiro = velocidade_cruzeiro
        self.num_motores = num_motores
        self.tipo_motor = tipo_motor  # "turbine" ou "reciprocating"
        self.preco_aeronave = preco_aeronave
        self.bloco_horas = bloco_horas
        self.horas_voo_anuais = horas_voo_anuais
        self.taxa_seguro = taxa_seguro  # Taxa do seguro da fuselagem

        # Dicionário de fatores de senioridade
        self.fator_senioridade = {"iniciante": 1.0, "pleno": 1.3, "sênior": 1.75}

        # Aplicação dos fatores de senioridade aos salários
        self.salarios_tripulacao = {
            "piloto": salario_piloto_iniciante * self.fator_senioridade[senioridade_piloto],
            "copiloto": salario_copiloto_iniciante * self.fator_senioridade[senioridade_copiloto],
            "engenheiro_voo": salario_eng_voo_iniciante * self.fator_senioridade[senioridade_eng_voo],
            "comissario": salario_comissario_iniciante * self.fator_senioridade[senioridade_comissario],
        }

        self.num_tripulacao = {
            "piloto": num_pilotos,
            "copiloto": num_copilotos,
            "engenheiro_voo": num_eng_voo,
            "comissario": num_comissarios,
        }

        self.despesas_viagem = {
            "piloto": despesas_viagem_piloto,
            "copiloto": despesas_viagem_copiloto,
            "engenheiro_voo": despesas_viagem_eng_voo,
            "comissario": despesas_viagem_comissario,
        }

        # Parâmetros de combustível e óleo
        self.combustivel_usado = combustivel_usado  # Consumo de combustível em libras
        self.preco_combustivel = preco_combustivel  # Preço do combustível por galão (USD/gal)
        self.densidade_combustivel = densidade_combustivel  # Densidade do combustível (lbs/gal)
        self.preco_oleo = preco_oleo  # Preço do óleo em USD/gal
        self.densidade_oleo = densidade_oleo  # Densidade do óleo em lbs/gal

        # Inicialização dos custos
        self.DOC_flt = 0  # Custo de voo
        
        
    """
######################################################################################## 
     DOC_flt   -> Custo direto de voo (tripulação, combustível e seguro)      
#####################################################################################  
       """       
        
    def calcular_custo_tripulacao(self, fator_k=0.0): # k 0.0, pois já está imbutido no salário as texas trabalhistas

        """
  Calcula o custo da tripulação por milha náutica com base na equação de Roskam:
  
  C_crew = SUM [(n_cj * (1 + K_j) / V_bl) * (SAL_j / AH_j) + (TEF_j / V_bl)]
  
  Onde:
      
  - n_cj: Número de tripulantes do tipo j (piloto, copiloto, engenheiro de voo, comissário)
  - K_j: Fator que inclui férias, treinamento e impostos sobre folha de pagamento (default = 0.26)
  - V_bl: Velocidade de bloco da aeronave em nós (aproximamos como V_cruise)
  - SAL_j: Salário anual do tripulante do tipo j (USD/ano)
  - AH_j: Número de horas de voo anuais para tripulantes
  - TEF_j: Despesas de viagem por tripulante (USD/hora de bloco)
  
  """
               
        velocidade_bloco = self.velocidade_cruzeiro  # Aproximação: Vbl ≈ Vcruise
        custo_tripulacao = sum([
            (self.num_tripulacao[cargo] * (1 + fator_k) / velocidade_bloco) * 
            (self.salarios_tripulacao[cargo] / self.horas_voo_anuais) + 
            (self.despesas_viagem[cargo] / velocidade_bloco)
            for cargo in ["piloto", "copiloto", "engenheiro_voo", "comissario"]
        ])
        self.DOC_flt += custo_tripulacao
        
        return custo_tripulacao
        

    def calcular_custo_combustivel_oleo(self):

        """
 Calcula o custo do combustível e óleo por milha náutica com base nas equações de Roskam.

 Fórmula utilizada para o custo do combustível:
     
 C_pol = (W_Fbl / R_bl) * (FP / FD)

 Onde:
     
 - W_Fbl  = Quantidade de combustível usado na missão (lbs)
 - R_bl   = Distância percorrida no bloco de voo (milhas náuticas)
 - FP     = Preço do combustível (USD/galão)
 - FD     = Densidade do combustível (lbs/galão)

 Fórmula utilizada para o consumo de óleo, que varia conforme o tipo de motor:

 Para motores recíprocos:
     
 W_olbl = W_Fbl / 70

 Para motores a turbina:
     
 W_olbl = 0.70 * N_e * t_bl

 Onde:
     
 - W_olbl = Peso do óleo e lubrificantes consumidos na missão (lbs)
 - N_e    = Número de motores da aeronave
 - t_bl   = Tempo de bloco em horas

 O custo do óleo é calculado como:
     
 C_ol = (W_olbl / R_bl) * (OLP / OD)

 Onde:
     
 - OLP = Preço do óleo e lubrificantes (USD/galão)
 - OD  = Densidade do óleo (lbs/galão)
 """
        
        
        distancia_bloco = self.velocidade_cruzeiro * self.bloco_horas  # R_bl = V_bl * t_bl

        # Consumo de combustível
        consumo_combustivel_nm = self.combustivel_usado / distancia_bloco  # W_Fbl / R_bl
        custo_combustivel = consumo_combustivel_nm * (self.preco_combustivel / self.densidade_combustivel)

        # Consumo de óleo baseado no tipo de motor
        if self.tipo_motor == "reciprocating":
            consumo_oleo_nm = self.combustivel_usado / (70 * distancia_bloco)  # Método para motores recíprocos
        else:  # Motores a turbina
            consumo_oleo_nm = (0.70 * self.num_motores * self.bloco_horas) / distancia_bloco  # Método para turbina

        custo_oleo = consumo_oleo_nm * (self.preco_oleo / self.densidade_oleo)

        self.DOC_flt += custo_combustivel + custo_oleo
        
        return self.DOC_flt

        
    def calcular_custo_seguro(self):
        
        """
        Calcula o custo do seguro da fuselagem por milha náutica com base na equação:
        
        C_ins = (f_ins_hull * AMP) / (U_annbl * V_bl)
        
        Onde:
        - f_ins_hull = Taxa de seguro da fuselagem por ano (USD/USD/aeronave/ano)
        - AMP = Preço de mercado da aeronave (USD)
        - U_annbl = Utilização anual de bloco de horas (horas/ano)
        - V_bl = Velocidade de bloco (nm/h)
        """
        velocidade_bloco = self.velocidade_cruzeiro  # Aproximação V_bl ~ V_cruise
        custo_seguro = (self.taxa_seguro * self.preco_aeronave) / (self.horas_voo_anuais * velocidade_bloco)
        self.DOC_flt += custo_seguro
    
        return custo_seguro

           
       
   
        
  