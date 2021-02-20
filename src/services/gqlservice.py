from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.websockets import WebsocketsTransport
import time
from jwt import encode
from os import getenv

event_id = str(getenv("EVENT_ID", "virtual-codeday-winter-2021"))


class GQLService:

    @staticmethod
    def make_token():
        secret = getenv("GQL_SHOWCASE_SECRET")
        message = {
            "a": True,
            "exp": int(time.time()) + (60*60*24*5),
            "aud": "showcase",
        }
        return encode(message, secret, algorithm='HS256').decode("utf-8")

    @staticmethod
    def make_query(query, with_fragments=True):
        if not with_fragments:
            return gql(query)

        fragments = """
                fragment ProjectInformation on ShowcaseProject {
                    id
                    name
                    type
                    description
                    pod: metadataValue(key: "pod")
                    members {
                        username
                        account {
                            discordId
                        }
                    }
                }
            """
        return gql(query + "\n" + fragments)

    @staticmethod
    async def query_http(query, variable_values=None, with_fragments=True):
        transport = AIOHTTPTransport(
            url="https://graph.codeday.org/",
            headers={"X-Showcase-Authorization": f"Bearer {GQLService.make_token()}"})
        client = Client(transport=transport, fetch_schema_from_transport=True)
        return await client.execute_async(GQLService.make_query(query, with_fragments=with_fragments), variable_values=variable_values)

    @staticmethod
    async def subscribe_ws(query, variable_values=None, with_fragments=True):
        transport = WebsocketsTransport(
            url='ws://graph.codeday.org/subscriptions')
        session = Client(transport=transport, fetch_schema_from_transport=True)
        async for result in session.subscribe_async(GQLService.make_query(query, with_fragments=with_fragments), variable_values=variable_values):
            yield result

    @staticmethod
    async def get_all_showcase_teams():
        query = """
            query getAllShowcaseTeamsWithoutPods($eventGroup: String!) {
              showcase {
                projects(where: {eventGroup: $eventGroup}) {
                    ...ProjectInformation
                }
              }
            }
        """

        params = {"eventGroup": event_id}

        result = await GQLService.query_http(query, variable_values=params)
        return result['showcase']['projects']

    @staticmethod
    async def get_all_showcase_teams_without_pods():
        print(event_id)
        query = """
            query getAllShowcaseTeamsWithoutPods($eventGroup: String!) {
              showcase {
                projects(where: {eventGroup: $eventGroup}) {
                    ...ProjectInformation
                }
              }
            }
        """

        params = {"eventGroup": event_id}

        result = await GQLService.query_http(query, variable_values=params)
        return [p for p in result["showcase"]["projects"] if (not ("pod" in p) or p["pod"] == None)]

    @staticmethod
    async def get_showcase_team_by_id(team_id):
        query = """
            query getShowcaseTeamById($id: String!) {
              showcase {
                project(id: $id) {
                    ...ProjectInformation
                }
              }
            }
        """

        params = {"id": team_id}

        # Execute the query on the transport
        result = await GQLService.query_http(query, variable_values=params)
        return result["showcase"]["project"]

    @staticmethod
    async def get_showcase_team_by_showcase_user(username):
        query = """
            query getShowcaseTeamByUser($eventGroup: String!, $username: String!) {
              showcase {
                projects(where: {eventGroup: $eventGroup user: $username}) {
                    ...ProjectInformation
                }
              }
            }
        """

        params = {"eventGroup": event_id, "username": username}

        # Execute the query on the transport
        result = await GQLService.query_http(query, variable_values=params)
        return result["showcase"]["projects"]

    @staticmethod
    async def get_showcase_user_from_discord_id(discord_id):
        query = """
            query getDiscordIdFromShowcaseUsername($discordId: String) {
              account {
                getUser(where: {discordId: $discordId}) {
                    username
                    discordId
                }
              }
            }
        """

        params = {"discordId": discord_id}

        # Execute the query on the transport
        result = await GQLService.query_http(query, variable_values=params, with_fragments=False)
        return result["account"]["getUser"]

    @staticmethod
    async def record_pod_on_team_metadata(project_id, value):
        query = """
            mutation recordPodOnTeam($project_id: String!, $value: String!) {
                showcase {
                    setMetadata(project: $project_id, key: "pod", value: $value, visibility: PUBLIC)
                }
            }
            """

        params = {"project_id": project_id, "value": value}
        await GQLService.query_http(query, variable_values=params, with_fragments=False)

    @staticmethod
    async def record_pod_name_on_team_metadata(project_id, value):
        query = """
            mutation recordPodOnTeam($project_id: String!, $value: String!) {
                showcase {
                    setMetadata(project: $project_id, key: "pod.name", value: $value, visibility: PUBLIC)
                }
            }
            """

        params = {"project_id": project_id, "value": value}
        await GQLService.query_http(query, variable_values=params, with_fragments=False)

    @staticmethod
    async def unset_team_metadata(project_id):
        query = """
            mutation unsetTeamMetaData($project_id: String!) {
                showcase {
                    result1: unsetMetadata(project: $project_id, key: "pod")
                    result2: unsetMetadata(project: $project_id, key: "pod.name")
                }
            }
            """

        params = {"project_id": project_id}
        await GQLService.query_http(query, variable_values=params, with_fragments=False)

    @staticmethod
    async def send_team_reacted(project_id, member, value):
        query = """
            mutation teamReacted($project_id: String!, $member: String!, $value: Float!){
              showcase {
                recordMetric(project: $project_id, member: $member, name: "reaction", value: $value)
              }
            }
        """

        params = {"project_id": project_id, "member": member, "value": value}
        print(params)
        await GQLService.query_http(query, variable_values=params, with_fragments=False)

    """Everything beyond this point is related to GQL Subscriptions and Bot Listener Stuff"""

    @staticmethod
    async def member_removed_listener():
        query = """
            subscription {
              memberRemoved {
                  username
                  account {
                      discordId
                  }
                  project {
                      ...ProjectInformation
                  }
              }
            }
        """

        async for result in GQLService.subscribe_ws(query):
            yield result["memberRemoved"]

    @staticmethod
    async def member_added_listener():
        query = """
            subscription {
              memberAdded {
                  username
                  account {
                      discordId
                  }
                  project {
                      ...ProjectInformation
                  }
              }
            }
        """

        async for result in GQLService.subscribe_ws(query):
            yield result["memberAdded"]

    @staticmethod
    async def team_created_listener():
        query = """
            subscription {
              projectCreated {
                  ...ProjectInformation
              }
            }
        """

        async for result in GQLService.subscribe_ws(query):
            yield result["projectCreated"]

    @staticmethod
    async def team_edited_listener():
        query = """
            subscription {
              projectEdited {
                  ...ProjectInformation
              }
            }
        """

        async for result in GQLService.subscribe_ws(query):
            yield result["projectEdited"]
