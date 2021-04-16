"""

Alembic Exceptions

"""


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


"""

Finder Exceptions

"""


class NoPodNamesAvailable(Exception):
    """Exception raised for errors when no pod names are left to be used.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="There are no available pod names left to be used."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class NoMentorsAvailable(Exception):
    """Exception raised for errors when no mentors are left to be used.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="There are no available mentors left to be used."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


"""

Finder Exceptions

"""


class PodNotFound(Exception):
    """Exception raised for errors when no mentors are left to be used.

    Attributes:
        name -- name of the pod
        channel -- given discord.TextChannel to attempt to get pod name from
        message -- explanation of the error
    """

    def __init__(self, name, channel_id, message="A pod was not able to be found from the two following arguments."):
        self.name = name
        self.channel_id = channel_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.name} and {self.channel_id} -> {self.message}'


class TeamIDNotFound(Exception):
    """Exception raised for errors in the team ID.

    Attributes:
        team_id -- input pod_id that caused the error
        message -- explanation of the error
    """

    def __init__(self, team_id, message="The given team id was not able to be found from showcase"):
        self.pod_id = team_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.pod_id} -> {self.message}'


class NoTeamsWithoutPods(Exception):
    """Exception raised for errors in the team ID.

    Attributes:
        team_id -- input pod_id that caused the error
        message -- explanation of the error
    """

    def __init__(self, message="There are no teams without pods."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class NoTeamsWithoutPods(Exception):
    """Exception raised for errors in the team ID.

    Attributes:
        team_id -- input pod_id that caused the error
        message -- explanation of the error
    """

    def __init__(self, message="There are no teams without pods."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class TeamNotFound(Exception):
    """Exception raised for errors in TeamConverter.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Informational, no action required - Unable to find any teams, occurs in "
                               "TeamConverter.py when no discord member,channel id, or pod name had any teams."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'

class PodMergeFailed(Exception):
    """Exception raised for errors in TeamConverter.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, pod_from, pod_to, message="An error has occurred when merging the pods and has been caught."):
        self.pod_from = pod_from
        self.pod_to = pod_to
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.pod_from} -> {self.pod_to} : {self.message}'
