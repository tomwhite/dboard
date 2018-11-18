#!/usr/bin/env python3

import argparse

from dboard.visualization import create_reports

parser = argparse.ArgumentParser()
parser.add_argument('entries', help='The entries CSV file')
parser.add_argument('out_dir', help='The output directory')
args = parser.parse_args()

create_reports(args.entries, args.out_dir)
