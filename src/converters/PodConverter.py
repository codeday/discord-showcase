from discord.ext import commands

from services.podservice import PodService
from utils.exceptions import PodNameNotFound, PodTCNotFound


class PodConverter(commands.Converter):

    async def convert(self, ctx, argument):
        print("start")
        try:
            argument = int(argument)
        except ValueError:
            pass

        if isinstance(argument, str):
            argument.capitalize()
            pod = PodService.get_pod_by_name(argument)
            if pod is None:
                raise PodNameNotFound(argument)
            return pod
        elif isinstance(argument, int):
            pod = PodService.get_pod_by_channel_id(argument)
            if pod is None:
                raise PodTCNotFound(argument)
            return pod
        print("end")