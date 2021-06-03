from typing import Union

import discord

from db.models import Pod
from services.poddbservice import PodDBService
from utils.exceptions import PodNotFound, PodNameNotFound, PodIDNotFound, PodTCNotFound, NoPods

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
            pod = PodDBService.get_pod_by_channel_id(current_channel.id)
        else:
            pod = PodDBService.get_pod_by_name(pod_name)
        if pod is None and current_channel is not None and output:
            await current_channel.send(output_msg)
            if raise_exception_if_none:
                raise PodNotFound(pod_name, current_channel.id)
        return pod

    @staticmethod
    async def get_pod_by_name(pod_name, current_channel: discord.TextChannel = None, output=True,
                              output_msg=f"A pod was not able to be found by the given name.",
                              raise_exception_if_none=False) -> Union[Pod, None]:
        """
        Takes the pod_name and attempts to find the pod from alembic. If it finds nothing,
        it raises a PodNameNotFound exception message to the current_channel.
        """
        pod = PodDBService.get_pod_by_name(pod_name)
        if pod is None and current_channel is not None and output:
            await current_channel.send(output_msg)
            if raise_exception_if_none:
                raise PodNameNotFound(pod_name)
        return pod

    @staticmethod
    async def get_pod_by_channel_id(channel_id, current_channel: discord.TextChannel = None,
                                    output=True,
                                    output_msg=f"A pod was not able to be found by the current channel.",
                                    raise_exception_if_none=False) -> Union[Pod, None]:
        """
        Takes the pod_id and attempts to find the pod from alembic. If it finds nothing,
        it returns None and sends a message to the current_channel.
        """
        pod = PodDBService.get_pod_by_channel_id(channel_id)
        if pod is None and current_channel is not None and output:
            await current_channel.send(output_msg)
            if raise_exception_if_none:
                raise PodTCNotFound(channel_id)
        return pod

    @staticmethod
    async def get_pod_by_id(pod_id, current_channel: discord.TextChannel = None,
                            output=True,
                            output_msg=f"A pod was not able to be found by the given pod ID.",
                            raise_exception_if_none=False) -> Union[Pod, None]:
        """
        Takes the pod_id and attempts to find the pod from alembic. If it finds nothing,
        it returns None and sends a message to the current_channel.
        """
        pod = PodDBService.get_pod_by_id(pod_id)
        if pod is None and current_channel is not None and output:
            await current_channel.send(output_msg)
            if raise_exception_if_none:
                raise PodIDNotFound(pod_id)
        return pod

    @staticmethod
    async def get_all_pods(current_channel: discord.TextChannel = None,
                           output=True,
                           output_msg=f"There are no pods to do the current action with.",
                           raise_exception_if_none=False) -> Union[list, None]:
        """
        Attempts to find all the pods from alembic. If it finds nothing,
        it returns None and sends a message to the current_channel.
        """
        pods = PodDBService.get_all_pods()
        if (pods is None or len(pods) == 0) and current_channel is not None and output:
            await current_channel.send(output_msg)
            if raise_exception_if_none:
                raise NoPods(pods)
        return pods

    @staticmethod
    def is_pod(pod_name) -> bool:
        if pod_name is None:
            return False
        return True if PodDBService.get_pod_by_name(pod_name) is not None else False
