from dboard import timeseries
import pytest


def test_read_entries_df():
    df = timeseries.read_entries_df("tests/entries.csv")
    row0 = df.iloc[0]
    assert row0.ts is not None
    assert row0.type == "sgv"
    assert row0.bg == pytest.approx(6.38889)
