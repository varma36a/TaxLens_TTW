def apply_nol(adjusted_income, nol_carryforward):
    max_nol = adjusted_income * 0.80
    nol_used = min(nol_carryforward, max_nol)
    return adjusted_income - nol_used