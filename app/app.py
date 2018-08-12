import os
import falcon
import argparse
import sqlalchemy

from sqlalchemy.orm import sessionmaker
from middleware import SQLAlchemySessionManager
from resources import TimeSeriesResource


engine = sqlalchemy.create_engine(os.environ['DATABASE_URL'])
session_factory = sessionmaker(bind=engine)

app = falcon.API(middleware=[SQLAlchemySessionManager(session_factory)])
app.add_route('/timeseries', TimeSeriesResource())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', help='Run debug server', action='store_true')
    args = parser.parse_args()
    if args.debug:
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', 8000, app, use_debugger=True, use_reloader=True)
    else:
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', 8000, app, use_debugger=False, use_reloader=True)
