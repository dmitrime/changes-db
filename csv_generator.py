import datetime
import json
import random
import sys
import time


def genprops(i, t, r):
    return json.dumps({'property1': t, 'property2': 'ID {} Round {}'.format(i, r)})


def generate(nrounds, ntypes, nids):
    samples = []
    d = datetime.datetime.now()
    ts = int(time.mktime(d.timetuple()))
    types = ['Object%d' % n for n in range(1, ntypes+1)]

    for r in range(nrounds, -1, -1):
        for cur_id in range(1, nids+1):
            for cur_type in types:
                samples.append((str(cur_id), cur_type, str(ts), genprops(cur_id, cur_type, r)))
                # add 1 second interval
                ts -= 1
    return samples

def write_csv(sm):
    print 'object_id | object_type | timestamp | object_changes'
    for s in sm:
        print ' | '.join(s)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Usage: {} N_rounds N_Types N_IDs'.format(sys.argv[0])
        sys.exit(1)

    rounds, types, ids = 0, 0, 0
    try:
        rounds = int(sys.argv[1])
        types = int(sys.argv[2])
        ids = int(sys.argv[3])
    except:
        print 'Arguments must be integer'
        sys.exit(1)

    samples = generate(rounds, types, ids)
    write_csv(samples)
