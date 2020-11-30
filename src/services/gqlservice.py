from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.websockets import WebsocketsTransport


class GQLService:

    @staticmethod
    def get_all_showcase_teams():
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

    @staticmethod
    def get_discord_users_by_team_id(team_id):
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url="https://graph.codeday.org/")

        # Create a GraphQL client using the defined transport
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Provide a GraphQL query
        query = gql(
            """
            query getContinents {
              continents {
                code
                name
              }
            }
        """
        )
        # Execute the query on the transport
        result = client.execute(query)
        return result

    @staticmethod
    def get_showcase_team_by_id(team_id):
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url="https://graph.codeday.org/")

        # Create a GraphQL client using the defined transport
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Provide a GraphQL query
        query = gql(
            """
            query getContinents {
              continents {
                code
                name
              }
            }
        """
        )
        # Execute the query on the transport
        result = client.execute(query)
        return result

    @staticmethod
    def get_showcase_team_by_user(username):
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url="https://graph.codeday.org/")

        # Create a GraphQL client using the defined transport
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Provide a GraphQL query
        query = gql(
            """
            query getShowcaseTeamByUser($code: ID!) {
              showcase {
                projects(code: $code) {
                  id
                  name
                }
              }
            }
        """
        )

        params = {"code": username}

        # Execute the query on the transport
        result = client.execute(query, variable_values=params)
        print(result)
        return result

    def member_removed(self):
        transport = WebsocketsTransport(url='ws://graph.codeday.org/')

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

        for result in client.subscribe(query):
            print(result)
