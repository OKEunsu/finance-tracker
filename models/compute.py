def safe_ratio(numer, denom):
    return numer / denom * 100 if denom != 0 else 0

def compute_financial_metrics(latest, previous=None):
    def extract_values(row):
        total_asset = row["CHECKING"] + row["ETC"] + row["INVESTMENT"] + row["SAVING"]
        total_debt = row["LOAN"]
        net_worth = total_asset + total_debt
        liquidity = row["CHECKING"] + row["ETC"]
        investment_ratio = safe_ratio(row["INVESTMENT"], total_asset)
        debt_ratio = safe_ratio(abs(total_debt), total_asset)
        liquidity_ratio = safe_ratio(liquidity, abs(total_debt))
        return total_asset, total_debt, net_worth, debt_ratio, liquidity_ratio, investment_ratio

    metrics = {}
    curr_vals = extract_values(latest)
    keys = ["총자산", "총부채", "순자산", "부채비율", "유동비율", "투자비중"]

    if previous is not None:
        prev_vals = extract_values(previous)
        for i, key in enumerate(keys):
            metrics[key] = (curr_vals[i], curr_vals[i] - prev_vals[i])
    else:
        for i, key in enumerate(keys):
            metrics[key] = (curr_vals[i], "–")

    return metrics
