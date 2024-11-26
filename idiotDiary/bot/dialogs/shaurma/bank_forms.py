from idiotDiary.bot.forms.shaurma import FshBankForms
from idiotDiary.bot.utils.dialog_factory import InputDialogFactory, WindowTemplate
from idiotDiary.bot.forms.shaurma.render.wrapper import as_render_callback


def setup():
    bank_dialogs = []
    window_template = WindowTemplate(add_main_menu_button=True)

    for device in FshBankForms:
        for from_bank in device.from_banks:
            for to_bank in from_bank.to_banks:
                bank_dialogs.append(
                    InputDialogFactory(
                        input_form=to_bank.form,
                        on_finish=as_render_callback(to_bank.render_func),
                        template=window_template
                    ).dialog()
                )

    return bank_dialogs
