from adaptix import Retort, name_mapping, NameStyle
from dishka import Provider, Scope, provide


class RetortProvider(Provider):
    scope = Scope.APP

    @provide
    def get_retort(self) -> Retort:
        return Retort(
            recipe=[
                name_mapping(name_style=NameStyle.LOWER_KEBAB)
            ]
        )
