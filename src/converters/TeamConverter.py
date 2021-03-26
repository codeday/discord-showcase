from services.podgqlservice import PodGQLService
from utils.exceptions import TeamIDNotFound, NoTeamsWithoutPods


class TeamConverter:

    @staticmethod
    async def get_showcase_team_by_id(team_id):
        team = await PodGQLService.get_showcase_team_by_id(team_id)
        if team is None:
            raise TeamIDNotFound(team_id)
        return team

    @staticmethod
    async def get_all_showcase_teams_without_pods():
        teams = await PodGQLService.get_all_showcase_teams_without_pods()
        if teams is None:
            raise NoTeamsWithoutPods()
        return teams