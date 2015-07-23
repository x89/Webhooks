import json
from pprint import pprint

fh = open('json', 'r')
foo = json.load(fh)
fh.close()
pprint(foo['commits'])

