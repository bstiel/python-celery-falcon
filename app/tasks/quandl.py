import requests

from models import TimeSeries
from worker import app
from .base import Task


@app.task(bind=True, base=Task, name='fetch_data_from_quandl')
def fetch_data_from_quandl(self, timeseries_id):
    timeseries = self.session.query(TimeSeries).filter_by(id=timeseries_id).one()
    url = f'https://www.quandl.com/api/v3/datasets/{timeseries.database_code}/{timeseries.dataset_code}/data.json'
    response = requests.get(url)
    if not response.ok:
        self.session.query(TimeSeries).filter_by(id=timeseries_id).update({'status': 'error'})
        self.session.commit()
        raise ValueError(f'GET {url} returned unexpected response code: {response.status_code}')

    self.session.query(TimeSeries).filter_by(id=timeseries_id).update({
        'data': response.json(),
        'status': 'success'
    })
    self.session.commit()
