from dboard.visualization import dboard


def test_dboard(tmpdir):
    dboard("tests/entries.csv", str(tmpdir), bg_range=(3.9, 8))
    assert "TIR: 78.8%" in tmpdir.join("index.html").read()
