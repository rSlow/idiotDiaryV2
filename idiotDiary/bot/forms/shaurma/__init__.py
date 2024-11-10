from idiotDiary.bot.forms.shaurma import render
from .models.banks import FromSberbank, FromTinkoff, ToSberbank, ToTinkoff
from .models.devices import Android, IPhone, Device
from .sberbank import AndroidSberbankForm, IPhoneSberbankForm
from .tinkoff import AndroidTinkoffForm, IPhoneTinkoffForm


class BankListForm(list[Device]):
    def __getitem__(self, device_name: str):
        for item in self:
            if item.type_.name == device_name:
                return item
        raise KeyError(device_name)


FshBankForms: list[Device] = BankListForm([
    Android(
        FromSberbank(
            ToSberbank(
                render_func=render.android.from_sberbank.to_sberbank.render,
                form=AndroidSberbankForm
            )
        ),
        FromTinkoff(
            ToTinkoff(
                render_func=render.android.from_tinkoff.to_tinkoff.render,
                form=AndroidTinkoffForm
            )
        ),
    ),
    IPhone(
        FromSberbank(
            ToSberbank(
                render_func=render.iphone.from_sberbank.to_sberbank.render,
                form=IPhoneSberbankForm
            )
        ),
        FromTinkoff(
            ToTinkoff(
                render_func=render.iphone.from_tinkoff.to_tinkoff.render,
                form=IPhoneTinkoffForm
            )
        ),
    )
])
