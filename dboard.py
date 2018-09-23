#!/usr/bin/env python3

import argparse

from dboard.visualization import create_json_index

parser = argparse.ArgumentParser()
parser.add_argument('entries', help='The entries CSV file')
parser.add_argument('out_dir', help='The output directory')
parser.add_argument('--bg_lower', type=float, default=3.9, help='The lower blood glucose range (mmol/l)')
parser.add_argument('--bg_upper', type=float, default=7, help='The upper blood glucose range (mmol/l)')
args = parser.parse_args()

create_json_index(args.entries, args.out_dir, (args.bg_lower, args.bg_upper))
