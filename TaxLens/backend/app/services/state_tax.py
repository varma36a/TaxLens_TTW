from app.utils.constants import STATE_TAX_RATES, PASS_THROUGHS


def calculate_state_tax(company):
    taxable_income = max(0, company.gross_income - company.deductions)

    entity_class = "PassThrough" if company.entity_type in PASS_THROUGHS else "C-Corp"
    rate = STATE_TAX_RATES[company.state_code][entity_class]

    state_tax = taxable_income * rate

    if company.state_code == "CA" and state_tax < 800:
        state_tax = 800

    return state_tax