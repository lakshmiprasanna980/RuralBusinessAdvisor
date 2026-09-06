# finance.py


def calculate_finance(business, investment):

    business = str(business).strip().lower()

    try:
        investment = float(investment)
    except (ValueError, TypeError):
        investment = 0

    # ---------------------------------------------------------
    # BUSINESS ASSUMPTIONS
    # ---------------------------------------------------------

    assumptions = {

        "farmer": {
            "revenue_rate": 0.35,
            "expense_rate": 0.22,
            "score": 78
        },

        "farming": {
            "revenue_rate": 0.35,
            "expense_rate": 0.22,
            "score": 78
        },

        "poultry farming": {
            "revenue_rate": 0.45,
            "expense_rate": 0.30,
            "score": 75
        },

        "handicrafts": {
            "revenue_rate": 0.30,
            "expense_rate": 0.18,
            "score": 80
        },

        "retail": {
            "revenue_rate": 0.28,
            "expense_rate": 0.20,
            "score": 76
        },

        "daily farming": {
            "revenue_rate": 0.32,
            "expense_rate": 0.21,
            "score": 77
        }
    }

    selected = assumptions.get(
        business,
        {
            "revenue_rate": 0.30,
            "expense_rate": 0.20,
            "score": 70
        }
    )

    # ---------------------------------------------------------
    # FINANCIAL CALCULATION
    # ---------------------------------------------------------

    required_investment = investment

    monthly_revenue = investment * selected["revenue_rate"]

    monthly_expense = investment * selected["expense_rate"]

    monthly_profit = (
        monthly_revenue -
        monthly_expense
    )

    annual_profit = monthly_profit * 12

    # ---------------------------------------------------------
    # FUNDING GAP
    # ---------------------------------------------------------

    recommended_investment = investment * 1.10

    funding_gap = max(
        0,
        recommended_investment - investment
    )

    # ---------------------------------------------------------
    # PROFIT MARGIN
    # ---------------------------------------------------------

    if monthly_revenue > 0:

        profit_margin = (
            monthly_profit /
            monthly_revenue
        ) * 100

    else:

        profit_margin = 0

    # ---------------------------------------------------------
    # ROI
    # ---------------------------------------------------------

    if investment > 0:

        roi = (
            annual_profit /
            investment
        ) * 100

    else:

        roi = 0

    # ---------------------------------------------------------
    # BREAK EVEN
    # ---------------------------------------------------------

    if monthly_profit > 0:

        break_even = (
            investment /
            monthly_profit
        )

    else:

        break_even = None

    # ---------------------------------------------------------
    # VIABILITY
    # ---------------------------------------------------------

    viability_score = selected["score"]

    if investment <= 0:

        viability_score = 0

    if viability_score >= 75:

        risk_level = "Low"

    elif viability_score >= 50:

        risk_level = "Moderate"

    else:

        risk_level = "High"

    # ---------------------------------------------------------
    # RECOMMENDATION
    # ---------------------------------------------------------

    if viability_score >= 75:

        recommendation = (
            "The business shows good financial potential. "
            "Start at a manageable scale, monitor expenses "
            "and validate local market demand before expanding."
        )

    elif viability_score >= 50:

        recommendation = (
            "The business has moderate potential. "
            "Carefully control operating costs and validate "
            "customer demand before increasing investment."
        )

    else:

        recommendation = (
            "Further financial evaluation is recommended. "
            "Review costs, expected revenue and funding "
            "requirements before making a major investment."
        )

    # ---------------------------------------------------------
    # FUNDING STATUS
    # ---------------------------------------------------------

    if funding_gap > 0:

        funding_status = (
            "Additional funding may be useful for working "
            "capital and business expansion."
        )

    else:

        funding_status = (
            "The available investment is sufficient for "
            "the estimated starting requirement."
        )

    # ---------------------------------------------------------
    # RETURN RESULT
    # ---------------------------------------------------------

    return {

        "required_investment":
            round(required_investment, 2),

        "monthly_revenue":
            round(monthly_revenue, 2),

        "monthly_expense":
            round(monthly_expense, 2),

        "monthly_profit":
            round(monthly_profit, 2),

        "annual_profit":
            round(annual_profit, 2),

        "funding_gap":
            round(funding_gap, 2),

        "profit_margin":
            round(profit_margin, 2),

        "roi":
            round(roi, 2),

        "break_even":
            round(break_even, 2)
            if break_even is not None
            else None,

        "viability_score":
            viability_score,

        "risk_level":
            risk_level,

        "recommendation":
            recommendation,

        "funding_status":
            funding_status
    }