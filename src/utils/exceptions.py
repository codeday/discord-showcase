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
