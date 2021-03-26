from typing import Union

import discord

from db.models import Pod
from services.poddbservice import PodDBService

"""
    The purpose of this class will be to sanitize input and return an appropriate pod object from alembic if found.
"""


class PodConverter:

    @staticmethod
    def get_pod(current_channel: discord.TextChannel, pod_name=None) -> Union[Pod, None]:
        """
        Takes the current channel and an optional pod_name and attempts to find the pod from alembic from
        one of the arguments. If it finds nothing, it returns None and sends a message to the current_channel.
        """
        if pod_name is None:
            pod = PodDBService.get_pod_by_channel_id(str(current_channel.id))
        else:
            pod = PodDBService.get_pod_by_name(str(pod_name).capitalize())
        if pod is None:
            await current_channel.send("A pod was not able to be found by the text channel or by name.")
        return pod

    @staticmethod
    def get_pod_by_name(pod_name) -> Union[Pod, None]:
        """
        Takes the pod_name and attempts to find the pod from alembic. If it finds nothing,
        it returns None and sends a message to the current_channel.
        """
        pod = PodDBService.get_pod_by_name(str(pod_name).capitalize())
        return pod
