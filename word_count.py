import sys, re, mmap, os
from cardinality import HyperLogLogSketch

word_splitter = re.compile(r"<[^>]*>|[^a-zA-Z0-9]+")
bogus_word = re.compile(r"(^\s+$)|(^\d+$)")

def is_valid_word(word):
    return len(word) > 1 and not bogus_word.match(word)

def lazy_split(splitter, string):
    start = 0
    for match in splitter.finditer(string):
        if match.start() > start:
            yield string[start:match.start()]
        start = match.end()

def get_words(html):
    return word_splitter.split(html)
    #return lazy_split(word_splitter, html)

def count_distinct_words(words, max_size=2**32, error_rate=0.2):
    sketch = HyperLogLogSketch(max_size, error_rate)
    for word in words:
        sketch.add(word)
    return sketch.getNumberEstimate()

def make_count_table(fname, words):
    import tokyocabinet.hash as tch
    out = tch.Hash()
    out.open(fname, tch.HDBOWRITER | tch.HDBOCREAT)

    for word in words:
        out.addint(word, 1)

    out.close()

def all_words():
    dir_list = os.listdir('pages')
    print len(dir_list)
    for fname in dir_list:
        if not fname.endswith('.html'):
            continue
        print fname
        f = open(os.path.join('./pages', fname), 'r')
        for word in get_words(f.read()):
            if is_valid_word(word):
                yield word

#word_count = count_distinct_words(all_words())
#print word_count

make_count_table('word_counts.tch', all_words())
