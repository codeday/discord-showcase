from os import getenv

import discord

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
            if PodDBService.get_pod_by_mentor_id(str(member.id), False) is None:
                # Mentor is Suitable, return that mentor object
                return member
        raise NoMentorsAvailable()
