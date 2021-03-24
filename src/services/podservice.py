from typing import Optional

from sqlalchemy.exc import IntegrityError

from db.models import session_creator, Pod, Team
from utils.exceptions import PodNameNotFound, PodTCNotFound, PodIDNotFound, PodDeleteFailed, PodWithMentorIDNotFound

# The best way to handle session with a cmd program (discord bot) is to have a global session variable.
# Information on why that is can be found here: https://docs.sqlalchemy.org/en/13/orm/session_basics.html
session = session_creator()


class PodService:
    @staticmethod
    def get_pod_by_name(name) -> Optional[Pod]:
        """Returns the pod with the given name, or none if it doesn't exist"""
        pod = session.query(Pod).filter(Pod.name == name).first()
        if pod is None:
            raise PodNameNotFound(name)
        return pod

    @staticmethod
    def get_pod_by_channel_id(tc_id) -> Optional[Pod]:
        """Returns the pod with the given text channel id, or none if it doesn't exist"""
        pod = session.query(Pod).filter(Pod.tc_id == tc_id).first()
        return pod

    @staticmethod
    def get_pod_by_id(id) -> Optional[Pod]:
        """Returns the pod with the given id, or none if it doesn't exist"""
        pod = session.query(Pod).filter(Pod.id == id).first()
        return pod

    @staticmethod
    def get_all_pods() -> list:
        """Returns a list of pod objects"""
        try:
            pods = session.query(Pod).all()
            return pods
        except Exception:
            return False

    @staticmethod
    def create_pod(name, tc_id, mentor) -> bool:
        """Create a new pod"""
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
        for pod in PodService.get_all_pods():
            try:
                session.delete(pod)
                session.commit()
            except PodDeleteFailed:
                return False

    @staticmethod
    def remove_pod(pod_name):
        """Deletes A SINGULAR pod by NAME from Alembic"""
        pod = PodService.get_pod_by_name(pod_name)

        try:
            session.delete(pod)
            session.commit()
        except PodDeleteFailed:
            return False

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
    def get_team_by_showcase_id(showcase_id) -> Team:
        """returns a Team with the given showcase id, freshly created if it doesn't exist"""
        team = session.query(Team).filter(
            Team.showcase_id == showcase_id).first()
        if not team:
            PodService.create_team(showcase_id)
            team = session.query(Team).filter(
                Team.showcase_id == showcase_id).first()
            session.commit()
        return team

    @staticmethod
    def add_team_to_pod(pod, team_showcase_id):
        session.add(pod)
        team = PodService.get_team_by_showcase_id(team_showcase_id)
        team.pod = pod
        session.commit()

    @staticmethod
    def get_pod_by_mentor_id(mentor_id) -> Optional[Pod]:
        """Returns the pod with the given mentor, or none if it doesn't exist"""
        try:
            pod = session.query(Pod).filter(Pod.mentor == mentor_id).first()
            return pod
        except PodWithMentorIDNotFound(mentor_id):
            return False

    @staticmethod
    def get_smallest_pod(size=5):
        """returns the smallest pod under given team size"""
        pods = session.query(Pod).all()
        pods.sort(key=lambda x: len(x.teams))

        if len(pods[0].teams) <= (size - 1):
            return pods[0]
        else:
            return None
