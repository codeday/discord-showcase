from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


class GQLService:

    @staticmethod
    def get_discord_users_by_team_name(team_name):
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
