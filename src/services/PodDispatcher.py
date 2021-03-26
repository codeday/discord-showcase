import discord
from discord.ext import commands

from converters.PodConverter import PodConverter
from services.poddbservice import PodDBService, session
from services.podgqlservice import PodGQLService


class PodDispatcher:

    @staticmethod
    async def remove_pod(pod, channel_to_remove: discord.TextChannel) -> bool:
        for team in pod.teams:
            await PodGQLService.unset_team_metadata(team.showcase_id)
        PodDBService.remove_pod(pod.name)
        await channel_to_remove.delete()
        session.commit()
        return True

    @staticmethod
    async def remove_all_pods(category) -> bool:
        PodDBService.remove_all_pods()
        for channel in category.channels:
            await channel.delete()
        all_teams = await PodGQLService.get_all_showcase_teams()
        for team in all_teams:
            await PodGQLService.unset_team_metadata(team["id"])
        return True

    @staticmethod
    async def merge_pods(pod_from, pod_to):
        pass

    @staticmethod
    def create_pod(pod_name, text_channel_id, mentor_id):
        PodDBService.create_pod(str(pod_name).capitalize(), text_channel_id, mentor_id)

