from .main import grade


def prepare_tinkoff_sums(
        start_sum: int,
        transfer_sum: int,
):
    str_start_sum = grade(f"{start_sum:.2f}".replace(".", ",")) + " ₽"
    str_transfer_sum = grade(f"{transfer_sum}".replace(".", ",")) + " ₽"
    str_end_sum = grade(f"{round(start_sum - transfer_sum, 2):.2f}".replace(".", ",")) + " ₽"

    changing_string = f"{str_start_sum}         {str_end_sum}"

    return str_start_sum, str_transfer_sum, str_end_sum, changing_string
