from common.dialogs import WindowFactory, WindowTemplate
from ..settings import FSSettings
from ..utils.send_files import render_callback


def get_fsh_dialogs():
    dialogs = []
    for device in FSSettings:
        for from_bank in device.value.from_banks:
            for to_bank in from_bank.to_banks:
                dialogs.append(WindowFactory(
                    states_group=to_bank.states_group,
                    on_finish=render_callback(to_bank.render_func),
                    template=WindowTemplate(add_main_menu_button=True)
                ).create_dialog())
    return dialogs
