def create_amount_text(
        amount: int | float,
        with_suffix: bool = False,
        with_symbol: bool = True
):
    amount = f"{amount:.2f}".replace(".", ",")
    if not with_suffix:
        amount = amount.removesuffix(",00")
    if with_symbol:
        amount += " ₽"

    return amount
