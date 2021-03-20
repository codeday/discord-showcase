import discord
from discord.ext import commands

from services.podservice import PodService
from utils.exceptions import PodNameNotFound, PodTCNotFound


class PodConverter:

    @staticmethod
    async def get_pod(current_channel: discord.TextChannel, pod_name=None):
        if pod_name is None:
            pod = PodService.get_pod_by_channel_id(str(current_channel.id))
        else:
            pod = PodService.get_pod_by_name(str(pod_name).capitalize())
        if pod is None:
            await current_channel.send("A pod was not able to be found by the text channel or by name.")
        return pod

