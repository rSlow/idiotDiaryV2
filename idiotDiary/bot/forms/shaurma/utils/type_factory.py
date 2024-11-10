def name_type_factory(value: str):
    list_initials = value.split()
    if len(list_initials) == 0:
        raise ValueError

    last_initial = list_initials[-1]
    first_initials = list_initials[:-1]

    if len(last_initial) == 1:
        if last_initial.isalpha():
            last_initial += "."

    elif len(last_initial) > 2:
        last_initial = last_initial[0] + "."

    initials = first_initials + [last_initial]
    validated_name = " ".join(initials)
    return validated_name


def phone_type_factory(value: str):
    digits = list(filter(lambda v: v.isdigit(), value))

    try:
        if (digits[0] == "8" or digits[0] == "7") and len(digits) == 11:
            digits[0] = "+7"
        elif digits[0] == "9" and len(digits) == 10:
            digits.insert(0, "+7")
        else:
            raise ValueError
    except IndexError:
        raise ValueError

    return f"{digits[0]} " \
           f"({''.join(digits[1:4])})" \
           f" {''.join(digits[4:7])}" \
           f"-{''.join(digits[7:9])}" \
           f"-{''.join(digits[9:11])}"


def amount_type_factory(value: str):
    transfer_amount = value.replace(",", ".")
    if transfer_amount.find("."):
        return round(float(transfer_amount), 2)
    return int(transfer_amount)
