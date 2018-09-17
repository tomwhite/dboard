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

```
mongoexport -h <host> -d <database> -u <user> -p <password> \
  -c entries \
  --fields type,sgv,mbg,date,dateString \
  --type csv \
  -o /tmp/entries.csv
```

Run

```
python update.py
python3 -m http.server 8000
open http://localhost:8000/out
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