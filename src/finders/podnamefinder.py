from services.poddbservice import PodDBService
from text.podnames import PodNames
from utils.exceptions import NoPodNamesAvailable

"""
    The purpose of this class will be to find an appropriate pod name that has not been used yet.
"""


class PodNameFinder:

    @staticmethod
    def find_a_suitable_pod_name() -> str:
        for pod_name in PodNames.available_names:
            if PodDBService.get_pod_by_name(pod_name) is None:
                return pod_name
        raise NoPodNamesAvailable()
