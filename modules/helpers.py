from decimal import Decimal, ROUND_HALF_UP

def round_decimal(x):
  return x.quantize(Decimal(".01"), rounding=ROUND_HALF_UP)

def fmt_money(v):
    return round_decimal(Decimal(v))


def fmt_money3(v):
    return round(float(v),3)


def fmt_money2(v):
    return round(float(v),2)
