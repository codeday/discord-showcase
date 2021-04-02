from os import getenv


class EnvironmentVariables:
    # How many teams should be in a singular pod? Change that value here. Default is 5.
    TEAMS_PER_POD = int(getenv("TEAMS_PER_POD", 5))

    # The role in which the bot will pick a mentor from for each text channel
    STAFF_ROLE = int(getenv("ROLE_STAFF", 689960285926195220))

    # The role in which the bot will pick a mentor from for each text channel
    MENTOR_ROLE = int(getenv("ROLE_MENTOR", 782363834836975646))

    # The category in which the pods will reside
    CATEGORY = int(getenv("CATEGORY", 783229579732320257))

    # The event ID in which this bot will operate on
    EVENT_ID = str(getenv("EVENT_ID", "virtual-codeday-winter-2021"))





