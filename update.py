from dboard.visualization import create_json_index

csv_file = '/tmp/entries.csv'
out_dir = 'gs://tom-dboard'
bg_range = (3.9, 8)

create_json_index(csv_file, out_dir, bg_range)
