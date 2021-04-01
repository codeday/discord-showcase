from os import getenv

import discord

from services.poddbservice import PodDBService
from utils.exceptions import NoPodNamesAvailable, NoMentorsAvailable

"""
    The purpose of this class will be to find an appropriate mentor that has not been used yet.
"""

mentor_role = int(getenv("ROLE_MENTOR", 782363834836975646))


class MentorFinder:

    @staticmethod
    def find_a_suitable_mentor(ctx) -> discord.Member:
        guild: discord.Guild = ctx.guild
        role: discord.Role = guild.get_role(mentor_role)
        print(role.members)
        for member in role.members:
            if PodDBService.get_pod_by_mentor_id(str(member.id)) is None:
                # Mentor is Suitable, return that mentor object
                return member
        raise NoMentorsAvailable()
