from typing import Union

import discord

from services.poddbservice import PodDBService
from services.podgqlservice import PodGQLService
from utils.exceptions import TeamIDNotFound, NoTeamsWithoutPods, TeamNotFound

"""
    The purpose of this class will be to sanitize input and return an appropriate team object from GraphQL if found.
    More information on GQL can be found in PodGQLService, to write custom queries go to https://graph.codeday.org/
"""

class TeamConverter:

    @staticmethod
    async def get_showcase_team_by_id(team_id):
        team = await PodGQLService.get_showcase_team_by_id(team_id)
        if team is None:
            raise TeamIDNotFound(team_id)
        return team

    @staticmethod
    async def get_all_showcase_teams_without_pods():
        teams = await PodGQLService.get_all_showcase_teams_without_pods()
        if teams is None:
            raise NoTeamsWithoutPods()
        return teams

    @staticmethod
    async def get_teams(current_channel: discord.TextChannel,
                        pod_name_or_discord_user: Union[str, discord.Member] = None):
        if pod_name_or_discord_user is None:
            pod = PodDBService.get_pod_by_channel_id(current_channel.id)
            return pod.teams
        elif isinstance(pod_name_or_discord_user, discord.Member):
            user = await PodGQLService.get_showcase_user_from_discord_id(str(pod_name_or_discord_user.id))
            teams = await PodGQLService.get_showcase_team_by_showcase_user(user)
            return teams
        elif isinstance(pod_name_or_discord_user, str):
            pod = PodDBService.get_pod_by_name(pod_name_or_discord_user)
            return pod.teams
        await current_channel.send("Team(s) were not able to be found by the text channel or by name.")
        raise TeamNotFound()
