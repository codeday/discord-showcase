from os import getenv


class EnvironmentVariables:
    """
    TEAMS_PER_POD Environment Variable
    Description: Tells the bot how many teams should be in a singular pod
    Default Value: 5
    """
    TEAMS_PER_POD = int(getenv("TEAMS_PER_POD", 5))

    """
    STAFF_ROLE Environment Variable
    Description: Tells the bot to add this role to every pod channel
    Default Value: 689960285926195220, Staff role in the CodeDay Test Server
    """
    STAFF_ROLE = int(getenv("ROLE_STAFF", 689960285926195220))

    """
    MENTOR_ROLE Environment Variable
    Description: Tells the bot which role to pick from when choosing mentors for each pod
    Default Value: 782363834836975646, Mentor role in the CodeDay Test Server
    """
    MENTOR_ROLE = int(getenv("ROLE_MENTOR", 782363834836975646))

    """
    CATEGORY Environment Variable
    Description: Tells the bot which category the pods should reside in
    Default Value: 783229579732320257, Pods category in CodeDay Test Server
    """
    CATEGORY = int(getenv("CATEGORY", 783229579732320257))

    """
    EVENT_ID Environment Variable
    Description: Tells the bot which event to grab teams from in showcase (using gql queries)
    Default Value: virtual-codeday-winter-2021, latest event
    """
    EVENT_ID = str(getenv("EVENT_ID", "virtual-codeday-winter-2021"))

    """
    DEBUG_CHANNEL Environment Variable
    Description: Tells the bot where to push testing command output and errors(future update)
    Default Value: 691780764261548133, error-log text channel in the CodeDay Test Server
    """
    DEBUG_CHANNEL = int(getenv("DEBUG_CHANNEL", 691780764261548133))
