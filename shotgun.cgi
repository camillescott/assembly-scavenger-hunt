#! /usr/bin/python
import cgi
import random, sys
import hashlib

DEFAULT_READ_LENGTH=7
DEFAULT_COVERAGE=10
DEFAULT_MUTATION_RATE=0.02
DEFAULT_DO_SORT=True
DEFAULT_DO_PAIRED=False
DEFAULT_INSERT_SIZE=25
COUNT=False
DEFAULT_TEXT="""It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we had nothing before us, we were all going direct to heaven, we were all going direct the other way - in short, the period was so far like the present period, that some of its noisiest authorities insisted on its being received, for good or for evil, in the superlative degree of comparison only."""

REFERENCE=False

def clean(text):
    data = text.split('\n\n')

    x = []
    for k in data:
        k = k.lower()
        k = k.replace(' ', '_')
        k = k.replace('\n', '_')
        k = k.replace(',', '')
        k = k.replace('\'', '')
        k = k.replace('.', '')
        x.append(k)

    return x

def fragment(text, read_length, coverage, mutation_rate):
    data = clean(text)

    chooseme = []
    for n, i in enumerate(data):
        chooseme += [n] * len(i)

    n_samples = int(len(chooseme) * coverage / float(read_length) + 0.5)

    samples = []
    for i in range(n_samples):
        seq = data[random.choice(chooseme)]

        start = random.choice(range(len(seq) - read_length))
        read = seq[start:start + read_length]

        for k in range(0, read_length):
            if random.uniform(0, 1000) < mutation_rate*1000:
                pos = random.choice(range(len(read)))
                s = ""
                for p in range(len(read)):
                    if p == pos:
                        s += random.choice('abcdefghijklmnopqrstuvwxyz_')
                    else:
                        s += read[p]
                read = s

        samples.append(read)

    return samples

def fragment_pe(text, read_length, insert_size, coverage, mutation_rate):
    data = clean(text)

    chooseme = []
    for n, i in enumerate(data):
        chooseme += [n] * len(i)

    n_samples = int(len(chooseme) * coverage / float(read_length) + 0.5)

    samples = []
    for i in range(n_samples):
        seq = data[random.choice(chooseme)]

        start = random.choice(range(len(seq) - insert_size))
        Lactual = insert_size - read_length + random.choice(range(2*read_length + 1))
        read = seq[start:start + Lactual]

        for k in range(0, insert_size):
            if random.uniform(0, 1000) < mutation_rate*1000:
                pos = random.choice(range(len(read)))
                s = ""
                for p in range(len(read)):
                    if p == pos:
                        s += random.choice('abcdefghijklmnopqrstuvwxyz_')
                    else:
                        s += read[p]
                read = s

        left, right = read[:read_length], read[-read_length:]
        samples.append((left, right))

    return samples

def convert_text(text):
    pass

def convert_dna(dna_text):
    pass

if __name__ == '__main__':
    coverage = DEFAULT_COVERAGE
    mutation_rate = DEFAULT_MUTATION_RATE
    read_length = DEFAULT_READ_LENGTH
    do_sort = DEFAULT_DO_SORT
    do_paired = DEFAULT_DO_PAIRED
    insert_size = DEFAULT_INSERT_SIZE

    form = cgi.FieldStorage()

    if 'cov' in form:
        coverage = float(form['cov'].value)
    if 'sorted' in form:
        if form['sorted'].value == 'yes':
            do_sort = True
        else:
            do_sort = False

    if 'readlen' in form:
        read_length = int(form['readlen'].value)

    if 'mut' in form:
        mutation_rate = float(int(form['mut'].value)) / 1000.

    if 'text' in form:
        text = form['text'].value
    else:
        text = DEFAULT_TEXT

    if 'paired' in form:
        if form['paired'].value == 'yes':
            do_paired = True
        else:
            do_paired = False

    if 'insert' in form:
        insert_size = int(form['insert'].value)

    h = hashlib.md5()
    cleaned = clean(text)
    for k in cleaned:
        h.update(k)
    digest = h.hexdigest()
    
    

    if not do_paired:
        samples = fragment(text, read_length, coverage, mutation_rate)
        if do_sort:
            samples.sort()

        print 'Content-type: text/html\n\n'
        print 'Text ID:', digest
        print '<!-- mut: %s / readlen: %d / cov: %s -->' % (mutation_rate,
                                                            read_length,
                                                            coverage)
        print '<pre>'
        for n, i in enumerate(samples):
            if n and n % 3 == 0:
                print '\n'
            print i + '            ',

        print ''
        print '</pre>'
    else:
        samples = fragment_pe(text, read_length, insert_size, coverage,
                              mutation_rate)
        if do_sort:
            samples.sort()

        print 'Content-type: text/html\n\n'
        print 'Text ID:', digest
        print '<!-- mut: %s / readlen: %d / cov: %s -->' % (mutation_rate,
                                                            read_length,
                                                            coverage)
        print '<pre>'
        for n, i in enumerate(samples):
            if n and n % 3 == 0:
                print '\n'
            print '%s, %s' % i + '            ',

        print ''
        print '</pre>'
