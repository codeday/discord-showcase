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
                        pod_name_or_discord_user: Union[str, discord.User] = None):
        print(pod_name_or_discord_user)
        if pod_name_or_discord_user is None:
            print("is none")
            teams = []
            pod = PodDBService.get_pod_by_channel_id(str(current_channel.id), False)
            for team in pod.teams:
                showcase_team = await TeamConverter.get_showcase_team_by_id(team.showcase_id)
                teams.append(showcase_team)
            if len(teams) == 0 or teams is None:
                await current_channel.send(
                    "There are no projects in your pod yet. Project(s) are still being created by attendee's.")
                raise TeamNotFound()
            return teams
        elif pod_name_or_discord_user[0] == "<":
            filter_out = "<!@>"
            for char in filter_out:
                pod_name_or_discord_user = pod_name_or_discord_user.replace(char, '')
            user = await PodGQLService.get_showcase_user_from_discord_id(str(pod_name_or_discord_user))
            teams = await PodGQLService.get_showcase_team_by_showcase_user(user['username'])
            if len(teams) == 0 or teams is None:
                await current_channel.send(f"<@{pod_name_or_discord_user}> does not belong to any projects.")
                raise TeamNotFound()
            return teams
        elif isinstance(pod_name_or_discord_user, str):
            print("is string")
            teams = []
            pod = PodDBService.get_pod_by_name(pod_name_or_discord_user)
            for team in pod.teams:
                showcase_team = await TeamConverter.get_showcase_team_by_id(team.showcase_id)
                teams.append(showcase_team)
            if len(teams) == 0 or teams is None:
                await current_channel.send(
                    "There are no projects in your pod yet. Project(s) are still being created by attendee's.")
                raise TeamNotFound()
            return teams
        await current_channel.send("Team(s) were not able to be found by the text channel or by name.")
        raise TeamNotFound()
