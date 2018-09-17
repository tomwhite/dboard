from dboard import stats
import pytest

data = ((0, 1, 2, 3, 4), (2.0, 5.0, 4.5, 10.0, 6.0))


def test_time_in_range():
    assert stats.time_in_range(data, (4.0, 7.0)) == pytest.approx(60.0)


def test_mean():
    assert stats.mean(data) == pytest.approx(5.5)


def test_estimated_hba1c():
    assert stats.estimated_hba1c(data) == pytest.approx(32.11, rel=1e-2)
