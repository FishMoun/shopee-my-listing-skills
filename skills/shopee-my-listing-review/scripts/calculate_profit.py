"""Calculate a single order scenario in MYR from explicit inputs."""
import json
import sys
from decimal import Decimal, DecimalException, ROUND_HALF_UP
from pathlib import Path

CENT = Decimal("0.01")


def number(value):
    result = Decimal(str(value))
    if not result.is_finite() or result < 0:
        raise ValueError("金额、汇率、基数和费率须为非负有限数")
    return result


def rounded(value):
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def percentage(value, base):
    return str(rounded(value / base * 100)) if base else None


def calculate(scenario):
    revenue = rounded(number(scenario["revenue_myr"]))
    amounts = {}

    def record(name, value):
        if not isinstance(name, str) or not name.strip() or name in amounts:
            raise ValueError("费用科目名称须非空且唯一")
        amounts[name] = rounded(value)

    for cost in scenario["costs"]:
        currency = cost["currency"]
        amount = number(cost["amount"])
        if currency == "CNY":
            rate = number(scenario["myr_per_cny"])
            if not rate:
                raise ValueError("CNY 折算需要大于 0 的 MYR/CNY 汇率")
            amount *= rate
        elif currency != "MYR":
            raise ValueError("费用币种须为 CNY 或 MYR")
        record(cost["name"], amount)

    for fee in scenario["fees"]:
        rate = number(fee["rate"])
        if rate > 1:
            raise ValueError("百分比费率请用 0 到 1 的小数")
        record(fee["name"], number(fee["base_myr"]) * rate)

    cost = sum(amounts.values(), Decimal("0.00"))
    profit = revenue - cost
    return {
        "revenue_myr": str(revenue),
        "costs_myr": {name: str(amount) for name, amount in amounts.items()},
        "total_cost_myr": str(cost),
        "profit_myr": str(profit),
        "cost_profit_rate_pct": percentage(profit, cost),
        "sales_margin_pct": percentage(profit, revenue),
    }


def main():
    if len(sys.argv) != 2:
        raise SystemExit("用法: python calculate_profit.py scenario.json")
    try:
        payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8-sig"), parse_float=Decimal)
        result = calculate(payload)
    except (OSError, DecimalException, KeyError, TypeError, ValueError) as exc:
        raise SystemExit(f"参数错误: {exc}") from exc
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
