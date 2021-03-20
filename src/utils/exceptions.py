class PodNameNotFound(Exception):
    """Exception raised for errors in the input name.

    Attributes:
        pod_name -- input name that caused the error
        message -- explanation of the error
    """

    def __init__(self, pod_name, message="The given pod name was not able to be found in alembic"):
        self.pod_name = pod_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.pod_name} -> {self.message}'


class PodTCNotFound(Exception):
    """Exception raised for errors in the tc_id.

    Attributes:
        tc_id -- input tc_id that caused the error
        message -- explanation of the error
    """

    def __init__(self, tc_id, message="The given pod tc_id was not able to be found in alembic"):
        self.tc_id = tc_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.tc_id} -> {self.message}'


class PodIDNotFound(Exception):
    """Exception raised for errors in the pod ID.

    Attributes:
        pod_id -- input pod_id that caused the error
        message -- explanation of the error
    """

    def __init__(self, pod_id, message="The given pod id was not able to be found in alembic"):
        self.pod_id = pod_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.pod_id} -> {self.message}'


class PodDeleteFailed(Exception):
    """Exception raised for errors in the pod ID.

    Attributes:
        pod -- input pod that caused the error
        message -- explanation of the error
    """

    def __init__(self, pod, message="A pod deletion was attempted and failed."):
        self.pod = pod
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.pod.name} -> {self.message}'


class PodWithMentorIDNotFound(Exception):
    """Exception raised for errors in the mentor ID.

    Attributes:
        mentor_id -- input mentor_id that caused the error
        message -- explanation of the error
    """

    def __init__(self, mentor_id, message="A pod with the given mentor ID was not found"):
        self.mentor_id = mentor_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.mentor_id} -> {self.message}'
