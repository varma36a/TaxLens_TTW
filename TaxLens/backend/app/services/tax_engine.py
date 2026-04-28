from app.services.federal_tax import calculate_federal_tax
from app.services.state_tax import calculate_state_tax
from app.services.qbi import calculate_qbi_deduction
from app.services.nol import apply_nol


def calculate_total_tax(company):
    federal_taxable_income = max(0, company.gross_income - company.deductions)

    adjusted_income = federal_taxable_income
    if company.entity_type in ["S-Corp", "LLC", "Partnership"]:
        qbi_deduction = calculate_qbi_deduction(federal_taxable_income)
        adjusted_income -= qbi_deduction

    final_taxable_income = apply_nol(adjusted_income, company.nol_carryforward)

    federal_tax = calculate_federal_tax(
        final_taxable_income,
        company.entity_type,
        company.credits
    )

    state_tax = calculate_state_tax(company)

    total_tax = federal_tax + state_tax
    effective_rate = (total_tax / company.gross_income) * 100 if company.gross_income > 0 else 0

    return {
        "federal_taxable_income": federal_taxable_income,
        "adjusted_taxable_income": adjusted_income,
        "final_taxable_income": final_taxable_income,
        "federal_tax": federal_tax,
        "state_tax": state_tax,
        "total_tax": total_tax,
        "effective_tax_rate": effective_rate
    }