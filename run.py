import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--init', action='store_true')

arg = parser.parse_args()
init = arg.init

if init:
    import src.json_to_postgres
else:
    import src
    src.app.run()
