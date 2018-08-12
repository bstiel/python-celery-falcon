import os
import celery
import sqlalchemy

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


class Task(celery.Task):

    def __call__(self, *args, **kwargs):
        self.engine = sqlalchemy.create_engine(os.environ['DATABASE_URL'])
        session_factory = sessionmaker(bind=self.engine)
        self.session = scoped_session(session_factory)
        return super().__call__(*args, **kwargs)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if hasattr(self, 'session'):
            self.session.remove()
        if hasattr(self, 'engine'):
            self.engine.engine.dispose()
