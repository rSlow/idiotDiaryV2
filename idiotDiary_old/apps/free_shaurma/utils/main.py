def grade(number: str):
    comma_index = number.find(",")

    if comma_index != -1:  # comma found
        integer = number[:comma_index]
        fractional = number[comma_index:]
    else:
        integer = number
        fractional = ""
    graded_number = ""
    for i, sym in enumerate(integer[::-1], 1):
        graded_number = sym + graded_number
        if i % 3 == 0:
            graded_number = " " + graded_number

    graded_number = graded_number.strip() + fractional
    return graded_number
