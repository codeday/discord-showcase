from services.podservice import PodService
from utils.exceptions import PodNameNotFound


class VerifyPod:
    """Contains information pertaining to Pods"""
    id = 0
    name = "Default"
    tc_id = ""
    mentor = ""
    teams = tuple()

    """Constructor to test if a pod is valid or not"""
    def __init__(self, name: str):
        name.capitalize()
        pod = PodService.get_pod_by_name(name)
        if pod is None:
            raise PodNameNotFound(name)

        self.name = name
        self.tc_id = pod.tc_id
        self.id = pod.id
        self.mentor = pod.mentor
        self.teams = pod.teams

    def __init__(self, tc_id: int):
        pod = PodService.get_pod_by_channel_id(tc_id)
        if pod is None:
            raise PodNameNotFound(name)

        self.name = pod.name
        self.tc_id = tc_id
        self.id = pod.id
        self.mentor = pod.mentor
        self.teams = pod.teams



