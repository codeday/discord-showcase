from typing import Union

import discord

from converters.PodConverter import PodConverter
from services.podgqlservice import PodGQLService
from utils.exceptions import TeamIDNotFound

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
        return teams

    @staticmethod
    async def get_teams(current_channel: discord.TextChannel,
                        pod_name_or_discord_user: str = None):
        if pod_name_or_discord_user is None:
            teams = []
            pod = await PodConverter.get_pod_by_channel_id(current_channel.id,
                                                           current_channel=current_channel)
            await TeamConverter.check_if_teams_exist(teams=pod.teams,
                                                     output_channel=current_channel,
                                                     output=f"There are no projects in Pod {pod.name} yet. Project(s) "
                                                            "are still being created by attendee's.")
            for team in pod.teams:
                showcase_team = await TeamConverter.get_showcase_team_by_id(team.showcase_id)
                teams.append(showcase_team)
            return teams
        elif pod_name_or_discord_user[0] == "<":  # discord username given
            filter_out = "<!@>"
            for char in filter_out:
                pod_name_or_discord_user = pod_name_or_discord_user.replace(char, '')
            user = await PodGQLService.get_showcase_user_from_discord_id(str(pod_name_or_discord_user))
            teams = await PodGQLService.get_showcase_team_by_showcase_user(user['username'])
            await TeamConverter.check_if_teams_exist(teams=teams,
                                                     output_channel=current_channel,
                                                     output=f"<@{pod_name_or_discord_user}> does not belong to any projects.")
            return teams
        else:  # assume pod name is given
            teams = []
            pod = await PodConverter.get_pod_by_name(pod_name=pod_name_or_discord_user,
                                                     current_channel=current_channel)

            await TeamConverter.check_if_teams_exist(teams=pod.teams,
                                                     output_channel=current_channel,
                                                     output=f"There are no projects in Pod {pod.name} yet.")
            for team in pod.teams:
                showcase_team = await TeamConverter.get_showcase_team_by_id(team.showcase_id)
                teams.append(showcase_team)
            return teams

    @staticmethod
    async def check_if_teams_exist(teams, output_channel: discord.TextChannel, output: str):
        if len(teams) == 0 or teams is None:
            await output_channel.send(output)
