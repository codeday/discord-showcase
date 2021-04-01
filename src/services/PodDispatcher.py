import discord

from services.poddbservice import PodDBService, session
from services.podgqlservice import PodGQLService
from utils.exceptions import PodMergeFailed
from utils.generateembed import GenerateEmbed
from utils.setpermissions import SetPermissions


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
    async def merge_pods(bot, pod_from, pod_to, from_channel, to_channel):
        if pod_from is not None and pod_to is not None:
            await from_channel.delete()
            if len(pod_from.teams) > 0:
                await to_channel.send("A pod is being merged into this channel...\n"
                                      "The projects joining this pod are: ")
                while len(pod_from.teams) > 0:
                    team = pod_from.teams[0]
                    await PodDispatcher.assign_pod(pod_to, team)
                    await to_channel.send(embed=GenerateEmbed.generate_embed(team))
                    await SetPermissions.for_channel_with_showcase_team(bot, to_channel, team)
                    await PodGQLService.unset_team_metadata(team.showcase_id)
                    await PodGQLService.record_pod_on_team_metadata(team.showcase_id, str(pod_to.id))
                    await PodGQLService.record_pod_name_on_team_metadata(team.showcase_id, str(pod_to.name))
            mentor = await bot.fetch_user(int(pod_to.mentor))
            await Pods.add_mentor_helper(bot, mentor, pod_to.name)
            PodDBService.remove_pod(pod_from.name)
            return
        raise PodMergeFailed(pod_from, pod_to)


    @staticmethod
    def create_pod(pod_name, text_channel_id, mentor_id):
        PodDBService.create_pod(str(pod_name).capitalize(), text_channel_id, mentor_id)

    @staticmethod
    async def assign_pod(pod, team):
        if pod is not None and team is not None:
            PodDBService.add_team_to_pod(pod, team["id"])
            await PodGQLService.record_pod_on_team_metadata(team["id"], str(pod.id))
            await PodGQLService.record_pod_name_on_team_metadata(team["id"], str(pod.name))

    @staticmethod
    def get_smallest_pod():
        return PodDBService.get_smallest_pod()
