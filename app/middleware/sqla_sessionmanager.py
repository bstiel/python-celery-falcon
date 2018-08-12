from sqlalchemy.orm import scoped_session

class SQLAlchemySessionManager:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def process_resource(self, req, resp, resource, params):
        resource.session = scoped_session(self.session_factory)

    def process_response(self, req, resp, resource, req_succeeded):
        if hasattr(resource, 'session'):
            resource.session.remove()