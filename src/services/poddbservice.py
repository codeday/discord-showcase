from typing import Optional

from sqlalchemy.exc import IntegrityError

from db.models import session_creator, Pod, Team
from utils.exceptions import PodNameNotFound, PodTCNotFound, PodIDNotFound, PodWithMentorIDNotFound

"""
    The purpose of this class is to query data from the Alembic database, for more information see below information.
    To see the Pod and Team data structure, go to the db/models.py file
"""

# The best way to handle session with a cmd program (discord bot) is to have a global session variable.
# Information on why that is can be found here: https://docs.sqlalchemy.org/en/13/orm/session_basics.html
session = session_creator()


class PodDBService:
    """
        Pod getter methods below, they simply return a pod if found or None if nothing is found
    """

    @staticmethod
    def get_pod_by_name(name: str) -> Optional[Pod]:
        """Returns the pod with the given name, or none if it doesn't exist"""
        pod = session.query(Pod).filter(Pod.name == name.lower().capitalize()).first()
        return pod

    @staticmethod
    def get_pod_by_channel_id(tc_id) -> Optional[Pod]:
        """Returns the pod with the given text channel id, or none if it doesn't exist"""
        pod = session.query(Pod).filter(Pod.tc_id == str(tc_id)).first()
        return pod

    @staticmethod
    def get_pod_by_id(_id) -> Optional[Pod]:
        """Returns the pod with the given id, or none if it doesn't exist"""
        pod = session.query(Pod).filter(Pod.id == id).first()
        return pod

    @staticmethod
    def get_pod_by_mentor_id(mentor_id) -> Optional[Pod]:
        """Returns the pod with the given mentor, or none if it doesn't exist"""
        pod = session.query(Pod).filter(Pod.mentor == mentor_id).first()
        return pod

    @staticmethod
    def get_smallest_pod() -> Optional[Pod]:
        """Returns the smallest pod under given team size or none if no pod is the smallest"""
        pods = session.query(Pod).all()
        pods.sort(key=lambda x: len(x.teams))

        return pods[0]

    @staticmethod
    def get_all_pods() -> list:
        """Returns a list of every pod object from Alembic"""
        pods = session.query(Pod).all()
        return pods

    @staticmethod
    def get_teams_by_showcase_id(showcase_id) -> Team:
        """Returns a Team with the given showcase id, freshly created if it doesn't exist"""
        team = session.query(Team).filter(
            Team.showcase_id == showcase_id).first()
        if not team:
            PodDBService.create_team(showcase_id)
            team = session.query(Team).filter(
                Team.showcase_id == showcase_id).first()
            session.commit()
        return team

    """
        Pod mutator methods below, these change something about the database
    """

    @staticmethod
    def create_pod(name, tc_id, mentor) -> bool:
        """Create a new pod"""
        name = str(name).lower().capitalize()
        try:
            session.add(
                Pod(
                    name=name,
                    tc_id=tc_id,
                    mentor=mentor,
                )
            )
            session.commit()
            return True
        except IntegrityError:
            return False

    @staticmethod
    def remove_all_pods():
        """Deletes ALL pods from Alembic"""
        for pod in PodDBService.get_all_pods():
            session.delete(pod)
            session.commit()

    @staticmethod
    def remove_pod(pod_name):
        """Deletes A SINGULAR pod by NAME from Alembic"""
        pod = PodDBService.get_pod_by_name(pod_name)
        session.delete(pod)
        session.commit()

    @staticmethod
    def create_team(showcase_id) -> bool:
        """Create a new team"""
        try:
            session.add(
                Team(
                    showcase_id=showcase_id
                )
            )
            session.commit()
            return True
        except IntegrityError:
            return False

    @staticmethod
    def add_team_to_pod(pod, team_showcase_id):
        """Simply adds a new team to a pod"""
        session.add(pod)
        team = PodDBService.get_teams_by_showcase_id(team_showcase_id)
        team.pod = pod
        session.commit()
