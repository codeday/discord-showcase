from typing import Optional

from sqlalchemy.exc import IntegrityError

from db.models import session_creator, Pod, Team


class TeamService:
    @staticmethod
    def get_pod_by_name(name, session=None) -> Optional[Pod]:
        """Returns the pod with the given name, or none if it doesn't exist"""
        sess_flag = False
        if session is None:
            session = session_creator()
            sess_flag = True
        pod = session.query(Pod).filter(Pod.name == name).first()
        if sess_flag:
            session.commit()
            session.close()
        return pod

    @staticmethod
    def get_pod_by_id(id, session=None) -> Optional[Pod]:
        """Returns the pod with the given id, or none if it doesn't exist"""
        sess_flag = False
        if session is None:
            session = session_creator()
            sess_flag = True
        pod = session.query(Pod).filter(Pod.id == id).first()
        if sess_flag:
            session.commit()
            session.close()
        return pod

    @staticmethod
    def get_all_pods(session=None) -> list:
        """Returns a list of team objects"""
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
    def add_pod(name, tc_id, mentor) -> bool:
        """Add a new pod"""
        try:
            session = session_creator()
            session.add(
                Pod(
                    name=name,
                    tc_id=tc_id,
                    mentor=mentor
                )
            )
            session.commit()
            session.close()
            return True
        except IntegrityError:
            return False