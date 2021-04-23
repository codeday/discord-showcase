from typing import Union

import discord

from db.models import Pod
from services.poddbservice import PodDBService
from utils.exceptions import PodNotFound, PodNameNotFound, PodIDNotFound

"""
    The purpose of this class will be to sanitize input and return an appropriate pod object from alembic if found.
"""


class PodConverter:

    @staticmethod
    async def get_pod(pod_name=None, current_channel: discord.TextChannel = None, output=True,
                      output_msg="A pod was not able to be found by the text channel or by name.",
                      raise_exception_if_none=False) -> Union[Pod, None]:

        """
        Takes the current channel and an optional pod_name and attempts to find the pod from alembic from
        one of the arguments. If it finds nothing, it returns None and sends a message to the current_channel.
        """
        if pod_name is None:
            pod = PodDBService.get_pod_by_channel_id(str(current_channel.id))
        else:
            pod = PodDBService.get_pod_by_name(str(pod_name).capitalize())
        if pod is None and output:
            await current_channel.send(output_msg)
            if raise_exception_if_none:
                raise PodNotFound(pod_name, current_channel.id)
        return pod

    @staticmethod
    def get_pod_by_name(pod_name, current_channel: discord.TextChannel = None, output=True,
                        output_msg=f"A pod was not able to be found by the given name.",
                        raise_exception_if_none=False) -> Union[Pod, None]:
        """
        Takes the pod_name and attempts to find the pod from alembic. If it finds nothing,
        it raises a PodNameNotFound exception message to the current_channel.
        """
        pod = PodDBService.get_pod_by_name(pod_name)
        if pod is None and output:
            await current_channel.send(output_msg)
            if raise_exception_if_none:
                raise PodNameNotFound(pod_name)
        return pod

    @staticmethod
    def get_pod_by_id(pod_id, current_channel: discord.TextChannel = None,
                      output=True,
                      output_msg=f"A pod was not able to be found by the given pod ID.",
                      raise_exception_if_none=False) -> Union[Pod, None]:
        """
        Takes the pod_id and attempts to find the pod from alembic. If it finds nothing,
        it returns None and sends a message to the current_channel.
        """
        pod = PodDBService.get_pod_by_id(pod_id)
        if pod is None and output:
            await current_channel.send(output_msg)
            if raise_exception_if_none:
                raise PodIDNotFound(pod_id)
        return pod

    @staticmethod
    def is_pod(pod_name) -> bool:
        return True if PodDBService.get_pod_by_name(pod_name) is not None else False
