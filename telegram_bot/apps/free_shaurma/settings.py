from enum import Enum

from .FSM import SberbankForm, TinkoffForm
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
                        states_group=SberbankForm
                    )
                ],
            ),
            FromTinkoff(
                to_banks=[
                    ToTinkoff(
                        render_func=render.android.tinkoff.tinkoff_tinkoff_phone_android,
                        states_group=TinkoffForm
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
                        states_group=SberbankForm
                    )
                ],
            ),
            FromTinkoff(
                to_banks=[
                    ToTinkoff(
                        render_func=render.iphone.tinkoff.tinkoff_tinkoff_phone_iphone,
                        states_group=TinkoffForm
                    )
                ],
            ),
        ]
    )
