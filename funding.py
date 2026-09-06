def get_funding_recommendation(
    business,
    investment,
    funding_gap,
    government_schemes
):

    business = str(business).strip().lower()

    try:
        investment = float(investment)
    except (ValueError, TypeError):
        investment = 0

    try:
        funding_gap = float(funding_gap)
    except (ValueError, TypeError):
        funding_gap = 0

    if funding_gap <= 0:
        return {
            "status": "No additional funding required",
            "recommended_source": "Own investment",
            "amount": 0,
            "reason": (
                "The available investment is sufficient "
                "for the estimated requirement."
            )
        }

    if government_schemes:
        source = "Government scheme / financial support"

        reason = (
            "The entrepreneur has a funding gap of "
            f"₹{funding_gap:,.0f}. Relevant government "
            "schemes should be evaluated before taking "
            "commercial credit."
        )

    else:
        source = "Bank or microfinance support"

        reason = (
            "A funding gap exists and no matching "
            "government scheme was identified. "
            "Bank or microfinance support can be "
            "considered after checking eligibility."
        )

    return {
        "status": "Additional funding recommended",
        "recommended_source": source,
        "amount": round(funding_gap, 2),
        "reason": reason
    }