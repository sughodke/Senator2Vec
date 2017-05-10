import glob
import json
from collections import defaultdict

from sklearn.externals import joblib

# TODO make these defaults otherwise read from sys.args
only_bills = False
house = 's'  # h

NAY = -1
YEA = +1

adj = defaultdict(dict)

for fname in glob.glob("congress/**/**/**/{}**/*json".format(house)):
    with open(fname) as f:
        print(fname)

        blob = json.load(f)
        votes = blob['votes']
        if only_bills:
            if 'bill' not in blob or blob['bill'] is None:
                continue

            bill = blob['bill']
            bill_num = '{session}-{bill}'.format(session=bill['congress'],
                                                 bill=bill['number'])

            nays = votes.get('Nay', [])
            yeas = votes.get('Yea', [])

            nays = map(lambda x: x['display_name'] if isinstance(x, dict) else x, nays)
            yeas = map(lambda x: x['display_name'] if isinstance(x, dict) else x, yeas)

            for n in nays:
                adj[bill_num][n] = NAY
            for y in yeas:
                adj[bill_num][y] = YEA
        else:
            vote_id = '{}-{}'.format(blob['congress'], blob['vote_id'])
            for option, voters in enumerate(votes.values()):
                # retain only the pretty name of the voters
                voters = map(lambda x: x['display_name'] if isinstance(x, dict) else x, voters)

                for voter in voters:
                    if '(' in voter:  # TODO better pattern match for expected Congressman format
                        adj[vote_id][voter] = option + 1


joblib.dump(adj, '{}-voting-matrix.npy'.format(house))

