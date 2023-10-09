import asyncio


async def stage_gather(
        *coroutines_or_futures,
        stage=50,
        return_exceptions=False):
    coroutines_or_futures_list = [*coroutines_or_futures]
    result_list = []

    while coroutines_or_futures_list:
        active_coroutines = coroutines_or_futures_list[:stage]
        coroutines_or_futures_list = coroutines_or_futures_list[stage:]

        stage_result = await asyncio.gather(
            *active_coroutines,
            return_exceptions=return_exceptions
        )
        result_list.extend(stage_result)

    return result_list
