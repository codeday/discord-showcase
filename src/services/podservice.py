from typing import Optional

from sqlalchemy.exc import IntegrityError

from db.models import session_creator, Pod, Team
from main import session
from utils.exceptions import PodNameNotFound, PodTCNotFound, PodIDNotFound


class PodService:
    @staticmethod
    def get_pod_by_name(name) -> Optional[Pod]:
        """Returns the pod with the given name, or none if it doesn't exist"""
        try:
            pod = session.query(Pod).filter(Pod.name == name).first()
            return pod
        except PodNameNotFound(name):
            return False

    @staticmethod
    def get_pod_by_channel_id(tc_id) -> Optional[Pod]:
        """Returns the pod with the given text channel id, or none if it doesn't exist"""
        try:
            pod = session.query(Pod).filter(Pod.tc_id == tc_id).first()
            return pod
        except PodTCNotFound:
            return False

    @staticmethod
    def get_pod_by_id(id) -> Optional[Pod]:
        """Returns the pod with the given id, or none if it doesn't exist"""
        try:
            pod = session.query(Pod).filter(Pod.id == id).first()
            return pod
        except PodIDNotFound:
            return False

    @staticmethod
    def get_all_pods(session=None) -> list:
        """Returns a list of pod objects"""
        sess_flag = False
        if session is None:
            session = session_creator()
            sess_flag = True
        pods = session.query(Pod).all()
        if sess_flag:
            session.commit()
            session.close()
        return pods

    @staticmethod
    def create_pod(name, tc_id, mentor) -> bool:
        """Create a new pod"""
        try:
            session = session_creator()
            session.add(
                Pod(
                    name=name,
                    tc_id=tc_id,
                    mentor=mentor,
                )
            )
            session.commit()
            session.close()
            return True
        except IntegrityError:
            return False

    @staticmethod
    def remove_all_pods():
        """Deletes ALL pods from Alembic"""
        session = session_creator()
        for pod in PodService.get_all_pods():
            session.delete(pod)

            session.commit()
            session.close()

    @staticmethod
    def remove_pod(name_of_pod):
        """Deletes A SINGULAR pod by NAME from Alembic"""
        session = session_creator()
        pod = PodService.get_pod_by_name(name_of_pod)
        session.delete(pod)
        session.commit()
        session.close()

    @staticmethod
    def create_team(showcase_id) -> bool:
        """Create a new team"""
        try:
            session = session_creator()
            session.add(
                Team(
                    showcase_id=showcase_id
                )
            )
            session.commit()
            session.close()
            return True
        except IntegrityError:
            return False

    @staticmethod
    def get_team_by_showcase_id(showcase_id, session=None) -> Team:
        """returns a Team with the given showcase id, freshly created if it doesn't exist"""
        sess_flag = False
        if session is None:
            session = session_creator()
            sess_flag = True
        team = session.query(Team).filter(
            Team.showcase_id == showcase_id).first()
        if not team:
            PodService.create_team(showcase_id)
            team = session.query(Team).filter(
                Team.showcase_id == showcase_id).first()
        if sess_flag:
            session.commit()
            session.close()
        return team

    @staticmethod
    def add_team_to_pod(pod, team_showcase_id, session=None):
        sess_flag = False
        if session is None:
            session = session_creator()
            sess_flag = True
        session.add(pod)
        team = PodService.get_team_by_showcase_id(team_showcase_id, session)
        team.pod = pod
        if sess_flag:
            session.commit()
            session.close()

    @staticmethod
    def get_pod_by_mentor_id(mentor_id, session=None) -> Optional[Pod]:
        """Returns the pod with the given mentor, or none if it doesn't exist"""
        sess_flag = False
        if session is None:
            session = session_creator()
            sess_flag = True
        pod = session.query(Pod).filter(Pod.mentor == mentor_id).first()
        if sess_flag:
            session.commit()
            session.close()
        return pod

    @staticmethod
    def get_smallest_pod(session=None, size=5):
        """returns the smallest pod under given team size"""
        sess_flag = False
        if session is None:
            session = session_creator()
            sess_flag = True
        pods = session.query(Pod).all()
        pods.sort(key=lambda x: len(x.teams))
        if sess_flag:
            session.commit()
            session.close()
        if len(pods[0].teams) <= (size-1):
            return pods[0]
        else:
            return None
