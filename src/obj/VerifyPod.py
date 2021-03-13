from services.podservice import PodService
from utils.exceptions import PodNameNotFound


class VerifyPod():
    """Contains information pertaining to Pods"""
    id = 0
    name = "Default"
    tc_id = ""
    mentor = ""

    """Constructor to test if a pod is valid or not"""
    def __init__(self, name: str):
        name.capitalize()
        pod = PodService.get_pod_by_name(name)
        if pod is None:
            raise PodNameNotFound(name)




