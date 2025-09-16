# -*- coding: utf-8 -*-
"""
Created on Wed May 28 13:22:36 2025

@author: ITA
"""

"""
capital_cost_calculator_caravan.py
---------------------------------
Python module to estimate the **capital‐cost component** of the Direct Operating
Cost (DOC) for a Cessna 208B Caravan (or similar regional aircraft) in three
acquisition scenarios:

1. **Loan‑financed purchase** (debt‑funded ownership)
2. **Operating lease**
3. **Outright purchase with own equity**

The implementation follows the *capital cost recovery* logic described by
Roskam (Airplane Design, Part VIII) and is fully commented so that each input
parameter and assumption is explicit.

Usage examples are provided at the bottom of the file under the
``if __name__ == "__main__":`` guard, so the script can be executed directly or
imported as a module in a larger DOC workflow.
"""
from dataclasses import dataclass
from typing import Literal

Scenario = Literal["loan", "lease", "own"]


def capital_recovery_factor(interest: float, years: int) -> float:
    """Compute the Capital Recovery Factor (CRF).

    CRF = i (1+i)^n / [(1+i)^n – 1]

    Args:
        interest: Annual nominal interest (or discount) rate as *decimal*
                  (e.g. 0.08 for 8 % a.a.).
        years: Economic life or loan term in whole years.

    Returns:
        CRF (dimensionless).
    """
    if years <= 0:
        raise ValueError("years must be positive")
    factor = (1 + interest) ** years
    return interest * factor / (factor - 1)


@dataclass
class CapitalCostInputs:
    """Container for common inputs across scenarios."""

    price_usd: float  # Aircraft acquisition price (USD)
    residual_fraction: float  # Residual value as fraction of price (e.g. 0.12)
    economic_life_yr: int  # Economic life of the hull (years)
    annual_hours: float  # Planned annual block hours
    block_speed_kts: float  # Average block speed (knots ≈ nm/h)
    
    
    ########## Compra financiada (empréstimo bancário ou linha de crédito para aeronaves);

    # Loan parameters (scenario = "loan") :     
    loan_pct: float = 0.8  # Fraction of price financed                         [proporção financiada]                          
    loan_interest: float = 0.06  # Nominal annual interest rate (decimal)       [ taxa de juros]
    loan_term_yr: int = 10  # Loan amortisation period (years)                  [prazo]

    ########## Leasing operacional (aluguel mensal);

    # Lease parameters (scenario = "lease")
    lease_rate_factor_monthly: float = 0.009  # Monthly LRF (decimal of price)  [LRF mensal]
    
    ######### Compra à vista (capital próprio).

    # Equity parameters (scenario = "own")
    wacc_equity: float = 0.08  # Opportunity cost of capital (decimal)          [custo de oportunidade indicado[]


@dataclass
class CapitalCostResult:
    """Results container with cost breakdown."""

    annual_cost_usd: float
    hourly_cost_usd: float
    cost_per_nm_usd: float


def compute_capital_cost(inputs: CapitalCostInputs, scenario: Scenario) -> CapitalCostResult:
    """Main API function.

    Args:
        inputs: CapitalCostInputs with all relevant parameters.
        scenario: "loan", "lease", or "own".

    Returns:
        CapitalCostResult with annual, hourly, and per‑nautical‑mile costs.
    """
    P = inputs.price_usd
    Vr = inputs.residual_fraction * P  # Residual value at end of life

    # Annual cost depends on the scenario
    # 1. **Loan** – paga-se juros sobre a parte financiada; a depreciação continua visível no DOC porque o ativo é seu.  
    # 2. **Lease** – paga-se um aluguel que já inclui tudo; depreciação e juros ficam “ocultos” dentro do LRF.  
    # 3. **Own** – não existe desembolso financeiro periódico, mas você “cobra” de si mesmo o custo do capital empatado (oportunidade).
    
     
    if scenario == "loan":
       # --- Loan‑financed purchase ---
       loan_amount = inputs.loan_pct * P      # principal financiado
        
       annual_interest = 0.5 * loan_amount * inputs.loan_interest
       # 0,5 ≅ saldo médio de um empréstimo que amortiza linearmente
        
       annual_cost = annual_interest              # NADA de amortização aqui
      # (a depreciação já aparecerá fora, como linha separada no seu DOC)



    elif scenario == "lease":
        # --- Operating lease ---
        annual_lease = P * inputs.lease_rate_factor_monthly * 12  # LRF is monthly
        annual_cost = annual_lease  # Lease already bundles depreciation + financing

    elif scenario == "own":
        
        # Juros apenas (custo de oportunidade) — depreciação fica em outra linha
        avg_book_value = 0.5 * (P + Vr)          # média entre valor inicial e residual
        annual_cost = avg_book_value * inputs.wacc_equity
        
        
        
       # annual_cost:  Cost of Equity (Custo do Capital Próprio) é a taxa de retorno mínima que os acionistas 
       # (ou qualquer investidor que aporte capital próprio) 
       # esperam ganhar para compensar o risco de manter seu dinheiro na empresa ou no projeto
        
    
        
        
    else:
        raise ValueError("scenario must be 'loan', 'lease', or 'own'")

    # Convert to hourly and per‑nautical‑mile costs
    hourly_cost = annual_cost / inputs.annual_hours
    cost_per_nm = hourly_cost / inputs.block_speed_kts

    return CapitalCostResult(
        annual_cost_usd=annual_cost,
        hourly_cost_usd=hourly_cost,
        cost_per_nm_usd=cost_per_nm,
    )


