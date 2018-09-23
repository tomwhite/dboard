# dboard

A dashboard for Type 1 Diabetes.

Visualize your blood glucose levels in a calendar-like view, with weekly summaries
of a few key metrics.

## Usage

Install Python dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Export data from Nightscout

```bash
mongoexport -h <host> -d <database> -u <user> -p <password> \
  -c entries \
  --fields type,sgv,mbg,date,dateString \
  --type csv \
  -o /tmp/entries.csv
```

Publish locally

```bash
./dboard.py --bg_lower 3.9 --bg_upper 8 /tmp/entries.csv out
python3 -m http.server 8000
open http://localhost:8000/out
```

Publish to Google Cloud

```bash
export GOOGLE_APPLICATION_CREDENTIALS=... # see https://cloud.google.com/docs/authentication/production#obtaining_and_providing_service_account_credentials_manually
./dboard.py --bg_lower 3.9 --bg_upper 8 /tmp/entries.csv gs://<bucket>
```

## Testing

```bash
pytest
```

Coverage
```bash
pip install pytest-cov
pytest --cov-report html --cov=dboard
open htmlcov/index.html
```