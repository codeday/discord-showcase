from os import getenv

import discord

from env import EnvironmentVariables
from services.poddbservice import PodDBService
from utils.exceptions import NoMentorsAvailable

"""
    The purpose of this class will be to find an appropriate mentor that has not been used yet.
"""


class MentorFinder:

    @staticmethod
    def find_a_suitable_mentor(role: discord.role) -> discord.Member:
        print(role.members)
        for member in role.members:
            if PodDBService.get_pod_by_mentor_id(str(member.id)) is None:
                # Mentor is Suitable, return that mentor object
                return member
        raise NoMentorsAvailable()

    @staticmethod
    async def enough_mentors_for_pod(ctx) -> bool:
        guild: discord.Guild = ctx.guild
        role: discord.Role = guild.get_role(EnvironmentVariables.MENTOR_ROLE)
        category = discord.utils.get(ctx.guild.categories, id=EnvironmentVariables.CATEGORY)
        if len(category.channels) >= len(role.members):
            await ctx.send("There are not enough additional mentors to fill more pods.")
            return False
        return True
