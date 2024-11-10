from enum import Enum

from .FSM import AndroidSberbankForm, AndroidTinkoffForm, IPhoneSberbankForm, IPhoneTinkoffForm
from .schemas.banks import FromSberbank, FromTinkoff, ToSberbank, ToTinkoff
from .schemas.devices import Android, IPhone
from .utils import render


class FSSettings(Enum):
    android = Android(
        from_banks=[
            FromSberbank(
                to_banks=[
                    ToSberbank(
                        render_func=render.android.sberbank.sberbank_sberbank_phone_android,
                        form=AndroidSberbankForm
                    )
                ],
            ),
            FromTinkoff(
                to_banks=[
                    ToTinkoff(
                        render_func=render.android.tinkoff.tinkoff_tinkoff_phone_android,
                        form=AndroidTinkoffForm
                    )
                ],
            ),
        ]
    )

    iphone = IPhone(
        from_banks=[
            FromSberbank(
                to_banks=[
                    ToSberbank(
                        render_func=render.iphone.sberbank.sberbank_sberbank_phone_iphone,
                        form=IPhoneSberbankForm
                    )
                ],
            ),
            FromTinkoff(
                to_banks=[
                    ToTinkoff(
                        render_func=render.iphone.tinkoff.tinkoff_tinkoff_phone_iphone,
                        form=IPhoneTinkoffForm
                    )
                ],
            ),
        ]
    )
