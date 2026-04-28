def progressive_tax(income, brackets):
    tax = 0
    previous_limit = 0

    for limit, rate in brackets:
        if income > limit:
            tax += (limit - previous_limit) * rate
            previous_limit = limit
        else:
            tax += (income - previous_limit) * rate
            break

    return tax


def calculate_federal_tax(income, entity_type, credits):
    if entity_type == "C-Corp":
        tax = income * 0.21
    else:
        brackets = [
            (11600, 0.10),
            (47150, 0.12),
            (100525, 0.22),
            (191950, 0.24),
            (243725, 0.32),
            (609350, 0.35),
            (float("inf"), 0.37)
        ]

        tax = progressive_tax(income, brackets)

    tax -= credits
    return max(0, tax)