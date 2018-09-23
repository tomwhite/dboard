from dboard.visualization import create_json_index


def test_dboard(tmpdir):
    create_json_index("tests/entries.csv", str(tmpdir), bg_range=(3.9, 8))
    assert '"tir": "78.8%"' in tmpdir.join("index.json").read()
