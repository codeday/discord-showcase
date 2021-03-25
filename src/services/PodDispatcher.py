from discord.ext import commands

from converters.PodConverter import PodConverter
from services.poddbservice import PodDBService


class PodDispatcher:

    @staticmethod
    async def send_message(bot, pod_name, *message):
        pod = PodConverter.get_pod_by_name(pod_name)
        pod_channel = await bot.fetch_channel(pod.tc_id)
        await pod_channel.send(" ".join(message[:]))

    @staticmethod
    async def send_message_all(bot, *message):
        all_pods = PodDBService.get_all_pods()
        for pod in all_pods:
            pod_channel = await bot.fetch_channel(pod.tc_id)
            await pod_channel.send(" ".join(message[:]))
