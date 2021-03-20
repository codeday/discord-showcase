import discord
from discord.ext import commands

from services.podservice import PodService
from utils.exceptions import PodNameNotFound, PodTCNotFound


class PodConverter(commands.Converter):

    async def convert(self, ctx, argument=None):
        print("start")
        if argument is None:
            current_channel: discord.TextChannel = ctx.channel
            pod = PodService.get_pod_by_id(str(current_channel.id))
        else:
            pod = PodService.get_pod_by_name(argument.capitalize())
        return pod
