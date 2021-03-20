import discord
from discord.ext import commands

from services.podservice import PodService
from utils.exceptions import PodNameNotFound, PodTCNotFound


class PodConverter(commands.Converter):

    async def convert(self, ctx, argument):
        print("start")
        pod = PodService.get_pod_by_name(argument.capitalize())
        if pod is None:
            current_channel: discord.TextChannel = ctx.channel
            pod = PodService.get_pod_by_id(current_channel.id)
        return pod