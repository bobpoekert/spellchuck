import tokyocabinet.hash as tch
import json, struct, math

_db = None
def db():
    global _db
    if not _db:
        _db = tch.Hash()
        _db.open('word_counts.tch')
    return _db

def get_int(db, key):
    try:
        return struct.unpack('I', db.get(key))[0]
    except:
        raise KeyError, key

def word_count(word):
    try:
        return get_int(db(), word)
    except KeyError:
        return 0

class CountArray(object):

    def __init__(self, prefix=''):
        self.db = db()
        self.keys = self.db.fwmkeys(prefix)

    def __iter__(self):
        for key in self.keys:
            yield get_int(self.db, key)

    def __getitem__(self, idx):
        key = self.keys[idx]
        return get_int(self.db, key)


def iteritems():
    f = db()
    for key in f.fwmkeys(''):
        yield key, get_int(f, key)

def generate_stats():
    f = db()
    _sum = 0
    sum2 = 0
    count = 0
    real_count = float(f.rnum())

    for key, val in iteritems():
        _sum += val
        sum2 += val * val
        count += 1

        if count % 1000 == 0:
            print '%d, %d%%' % (count, int(count / real_count * 100))

    json.dump(dict(
        sum=_sum,
        sum2=sum2,
        count=count), open('stats.json', 'w'))

_stats = None
def stats():
    global _stats
    if not _stats:
        _stats = json.load(open('stats.json', 'r'))
    return _stats

def count():
    s = stats()
    return s['count']

def mean():
    s = stats()
    return s['sum'] / s['count']

def std_deviation():
    s = stats()
    _sum = s['sum']
    return math.sqrt(s['count'] * s['sum2'] - s['sum'] * s['sum']) / s['count']

if __name__ == '__main__':
    generate_stats()
