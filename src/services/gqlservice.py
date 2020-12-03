from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.websockets import WebsocketsTransport


class GQLService:

    @staticmethod
    async def get_all_showcase_teams():
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url="https://graph.codeday.org/")

        # Create a GraphQL client using the defined transport
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Provide a GraphQL query
        query = gql(
            """
            query {
              showcase {
                projects {
                  id
                  name
                }
              }
            }
        """
        )
        # Execute the query on the transport
        result = await client.execute_async(query)
        print(result)
        return result['showcase']['projects']

    # NOT DONE
    @staticmethod
    def get_all_showcase_teams_without_pods():
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url="https://graph.codeday.org/")

        # Create a GraphQL client using the defined transport
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Provide a GraphQL query
        query = gql(
            """
            query {
              showcase {
                projects {
                  id
                  name
                }
              }
            }
        """
        )
        # Execute the query on the transport
        result = client.execute(query)
        return result

    # NOT DONE
    @staticmethod
    def get_showcase_team_by_id(team_id):
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url="https://graph.codeday.org/")

        # Create a GraphQL client using the defined transport
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Provide a GraphQL query
        query = gql(
            """
            query {
              showcase {
                project(id: "ckhwbqp2h006411mpd99ircmk") {
                  name
                  id
                  members {
                    username
                    account {
                      discordId
                    }
                  }
                }
              }
            }
        """
        )
        # Execute the query on the transport
        result = client.execute(query)
        return result


    @staticmethod
    async def get_showcase_team_by_showcase_user(username):
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url="https://graph.codeday.org/")

        # Create a GraphQL client using the defined transport
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Provide a GraphQL query
        query = gql(
            """
            query getShowcaseTeamByUser($username: String!) {
              showcase {
                projects(where: {user: $username}) {
                  id
                  name
                }
              }
            }
        """
        )

        params = {"username": username}

        # Execute the query on the transport
        result = await client.execute_async(query, variable_values=params)
        print(result)
        return result

    @staticmethod
    async def get_showcase_user_from_discord_id(discord_id):
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url="https://graph.codeday.org/")

        # Create a GraphQL client using the defined transport
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Provide a GraphQL query
        query = gql(
            """
            query getDiscordIdFromShowcaseUsername($discordId: String) {
              account {
                getUser(where: {discordId: $discordId}) {
                  username
                  id
                }
              }
            }
        """
        )

        params = {"discordId": discord_id}

        # Execute the query on the transport
        result = await client.execute_async(query, variable_values=params)
        print(result)
        return result

    @staticmethod
    async def send_team_reacted(project_id, member, name, value):
        transport = WebsocketsTransport(url='ws://graph.codeday.org/subscriptions')

        client = Client(
            transport=transport,
            fetch_schema_from_transport=True,
        )

        query = gql('''
            mutation teamReacted($project_id: String, $member: String, $name: String, $value: ID){
              showcase {
                recordMetric(project: $project_id, member: $member, name: $name, value: $value)
              }
            }
        ''')

        params = {"project_id": project_id, "member": member, "name": name, "value": value}

        async for result in client.subscribe_async(query, variable_values=params):
            print(result)

    """Everything beyond this point is related to GQL Subscriptions and Bot Listener Stuff"""

    @staticmethod
    async def member_removed_listener():
        transport = WebsocketsTransport(url='ws://graph.codeday.org/subscriptions')

        client = Client(
            transport=transport,
            fetch_schema_from_transport=True,
        )

        query = gql('''
            subscription {
              memberRemoved(where:{eventGroup:"virtual-2020-dec"}) {
                username
                account {
                  name
                  discordId
                }
              }
            }
        ''')

        async for result in client.subscribe_async(query):
            print(result)

    @staticmethod
    async def member_added_listener():
        transport = WebsocketsTransport(url='ws://graph.codeday.org/subscriptions')

        client = Client(
            transport=transport,
            fetch_schema_from_transport=True,
        )

        query = gql('''
            subscription {
              memberAdded(where:{eventGroup:"virtual-2020-dec"}) {
                username
                account {
                  name
                  discordId
                }
              }
            }
        ''')

        async for result in client.subscribe_async(query):
            print(result)

    @staticmethod
    async def team_created_listener():
        transport = WebsocketsTransport(url='ws://graph.codeday.org/subscriptions')

        client = Client(
            transport=transport,
            fetch_schema_from_transport=True,
        )

        query = gql('''
            subscription {
              projectCreated(where:{eventGroup:"virtual-2020-dec"}) {
                username
                account {
                  name
                  discordId
                }
              }
            }
        ''')

        async for result in client.subscribe_async(query):
            print(result)

    @staticmethod
    async def team_submitted_listener():
        transport = WebsocketsTransport(url='ws://graph.codeday.org/subscriptions')

        client = Client(
            transport=transport,
            fetch_schema_from_transport=True,
        )

        query = gql('''
            subscription {
              projectEdited(where:{eventGroup:"virtual-2020-dec"}) {
                username
                account {
                  name
                  discordId
                }
              }
            }
        ''')

        async for result in client.subscribe_async(query):
            print(result)