## Fetch Timeseries From Quandl With Celery and Falcon

1. Start stack: `docker-compose up -d`

2. Fetch timeseries from Quandl: `curl -d '{"database_code":"WIKI", "dataset_code":"FB"}' -H "Content-Type: application/json" -X POST http://localhost:8000`

3. List all timeseries: `curl -X GET http://localhost:8000`

4. Retrieve a timeseries: `curl -X GET http://localhost:8000?id=<...>`
