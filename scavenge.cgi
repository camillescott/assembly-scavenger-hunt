#! /usr/bin/python

import binascii
import random
import tempfile
import cgi
import os
import hashlib

DEFAULT_READ_LENGTH=50
DEFAULT_COVERAGE=10
DEFAULT_MUTATION_RATE=0.02
DEFAULT_DO_SORT=True
DEFAULT_DO_PAIRED=False
DEFAULT_INSERT_SIZE=100
DEFAULT_NOISE_RATIO=1.0
DEFAULT_NOISE_COVERAGE=5
DEFAULT_TEXT='''
THIS IS THE MOST BORING SCAVENGER HUNT!
'''

bin_to_dna_table = { '00':'A', '01':'G', '10':'C', '11':'T' }
dna_to_bin_table = { 'A':'00', 'G':'01', 'C':'10', 'T':'11' }

def text_to_bin(text):
    return bin(int(binascii.hexlify(text), 16))


def bin_to_text(bi):
    i = int(bi, 2)
    return binascii.unhexlify('%x' % i)

def bin_to_dna(bi):
    dna = ''
    for i in range(0,len(bi),2):
        dna += bin_to_dna_table[bi[i:i+1]]
    return dna

def dna_to_bin(dna):
	bi = ''
	for n in dna:
		bi += dna_to_bin(n)
	return bi

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

def random_seq(length):
    random.seed(1)

    x = ["A"] + ["G"] + ["C"] + ["T"]
    x = x*length
    random.shuffle(x)
    x = "".join(x)

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
    
def make_dir(tempdir):
    """
    Make a working directory.
    """
    dir = tempfile.mkdtemp('', 'reads.', tempdir)
    dirstub = dir[len(tempdir) + 1:]
    return dir, dirstub

def iter_text(text):
    tmp = text.split(sep='>')
    for line in tmp:
        cov, _, words = line.partition('|')
        if not cov.isdigit():
            cov = -1
            words = line
        yield cov, words

if __name__ == '__main__':
    coverage = DEFAULT_COVERAGE
    mutation_rate = DEFAULT_MUTATION_RATE
    read_length = DEFAULT_READ_LENGTH
    do_paired = DEFAULT_DO_PAIRED
    insert_size = DEFAULT_INSERT_SIZE
    noise_ratio = DEFAULT_NOISE_RATIO
    noise_coverage = DEFAULT_NOISE_COVERAGE

    form = cgi.FieldStorage()
    
    if 'cov' in form:
        coverage = float(form['cov'].value)

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
        
    if 'noise' in form:
        noise_ratio = float(form['noise'].value)
    
    if 'noise_cov' in form:
        noise_coverage = int(form['noise_cov'].value)
        
    h = hashlib.md5()
    cleaned = clean(text)
    for k in cleaned:
        h.update(k)
    digest = h.hexdigest()
    
    if not do_paired:
        tempdir, dirstub = make_dir('/home/cswelcher/public_html/tmp_files/reads')
        samples = []
        total_len = 0
        fn = os.path.join(tempdir, 'scavenger_reads.fa')
        with open(fn, 'wb') as outfp:
            for cov, words in iter_text(text):
                if cov == -1:
                    cov = DEFAULT_COVERAGE
                total_len += len(words)
                samples += fragment(words, read_length, cov, mutation_rate)
            if noise_ratio < 1.0:
                noise_len = (1.0/noise_ratio) * total_len
                noise_seq = random_seq(noise_len)
                samples += fragment(noise_seq, read_length, noise_coverage, mutation_rate)
            random.shuffle(samples)
            for i, read in enumerate(samples):
                outfp.write('>{}\n{}\n'.format(i, read))
        print 'Content-type: text/html\n\n'
        print 'Text ID:', digest
        print '<!-- mut: %s / readlen: %d / cov: %s -->' % (mutation_rate,
                                                            read_length,
                                                            coverage)
        print '<pre>'
        print 'Reads file: <a href="{}">scavenger_reads.fa</a>>'

        print ''
        print '</pre>'
            
            
