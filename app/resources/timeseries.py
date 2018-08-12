import falcon
import uuid
import json

from models import TimeSeries
from tasks.quandl import fetch_data_from_quandl


class TimeSeriesResource:

    def on_get(self, req, resp):
        if 'id' in req.params:
            timeseries = self.session.query(TimeSeries).filter(TimeSeries.id == req.params['id']).one()
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(timeseries.data)
        else:
            timeseries = [{
                'id': str(timeseries.id),
                'database_code': timeseries.database_code,
                'dataset_code': timeseries.dataset_code
             } for timeseries in self.session.query(TimeSeries).all()]
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(timeseries)
    
    def on_post(self, req, resp):
        body = req.stream.read()
        payload = json.loads(body.decode('utf-8'))
        database_code = payload['database_code']
        dataset_code = payload['dataset_code']

        timeseries = TimeSeries(
            id=uuid.uuid4(),
            database_code=database_code,
            dataset_code=dataset_code,
            data={},
            status='pending'
        )

        self.session.add(timeseries)
        self.session.commit()

        fetch_data_from_quandl.s(timeseries_id=timeseries.id).delay()
        resp.status = falcon.HTTP_201
        resp.body = json.dumps({
            'id': str(timeseries.id),
            'status': timeseries.status
        })