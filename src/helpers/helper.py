import discord

from converters.PodConverter import PodConverter
from converters.TeamConverter import TeamConverter
from env import EnvironmentVariables
from services.poddbservice import PodDBService
from services.podgqlservice import PodGQLService
from utils.generateembed import GenerateEmbed
from utils.setpermissions import SetPermissions

"""
    The purpose of this class will be to help out certain classes such as pods.py and PodDispatcher, these are needed
    because it allows modularization and allows for other areas of code (such as s~merge_pods) to assign pods other 
    than when executing s~assign_pods. 
"""


class Helper:

    # Some notes about embedded messages:
    # - To display fields side-by-side, you need at least two consecutive fields set to inline
    # - The timestamp will automatically adjust the timezone depending on the user's device
    # - Mentions of any kind will only render correctly in field values and descriptions
    # - Mentions in embeds will not trigger a notification
    @staticmethod
    async def assign_pod_helper(bot: discord.ext.commands.Bot, team_id, pod_name):
        current_pod = PodConverter.get_pod_by_name(pod_name)
        showcase_team = await TeamConverter.get_showcase_team_by_id(team_id)
        print(showcase_team)

        if current_pod is not None and showcase_team is not None:
            PodDBService.add_team_to_pod(current_pod, showcase_team["id"])
            await PodGQLService.record_pod_on_team_metadata(showcase_team["id"], str(current_pod.id))
            await PodGQLService.record_pod_name_on_team_metadata(showcase_team["id"], str(current_pod.name))

            tc = await bot.fetch_channel(int(current_pod.tc_id))

            await tc.send(embed=GenerateEmbed.for_single_showcase_team(showcase_team))
            await SetPermissions.for_channel_with_showcase_team(bot, tc, showcase_team)

    @staticmethod
    async def assign_pods_helper(bot: discord.ext.commands.Bot):
        all_teams_without_pods = await TeamConverter.get_all_showcase_teams_without_pods()

        for team in all_teams_without_pods:
            if len(team["members"]) >= 1:
                smallest_pod = PodDBService.get_smallest_pod()
                if len(smallest_pod.teams) < EnvironmentVariables.TEAMS_PER_POD:
                    await Helper.assign_pod_helper(bot, team["id"], smallest_pod.name)
                else:
                    await Helper.assign_pod_helper(bot, team["id"], "overflow")

    @staticmethod
    async def add_mentor_helper(bot: discord.ext.commands.Bot, mentor: discord.Member, pod_name=None, pod=None):
        if pod is None:
            pod = PodConverter.get_pod_by_name(pod_name)

        pod_channel: discord.TextChannel = await bot.fetch_channel(pod.tc_id)
        await pod_channel.set_permissions(mentor,
                                          overwrite=discord.PermissionOverwrite(**dict(discord.Permissions.text())))
        await pod_channel.send(
            "Hello <@" +
            str(mentor.id) +
            "> you have been added as a mentor to this pod! To see a list of teams, type s~teams")
