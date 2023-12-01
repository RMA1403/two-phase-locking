import argparse

from scheduler import Scheduler

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="file path")
args = parser.parse_args()

scheduler = Scheduler.from_file(args.file)

scheduler.generate_schedule()
scheduler.print_final_schedule()
