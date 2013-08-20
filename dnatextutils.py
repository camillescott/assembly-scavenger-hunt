#! /usr/bin/python

bin_to_dna_table = { '00':'A', '01':'G', '10':'C', '11':'T' }
dna_to_bin_table = { 'A':'00', 'G':'01', 'C':'10', 'T':'11' }

def text_to_bin(text):
    tmp = ''
    for c in text:
        bi = bin(ord(c))
        tmp += bi[2:].zfill(8)
    return tmp

def bin_to_text(bi):
    text = ''
    for i in range(0,len(bi),8):
        #print bi[i:i+8], int(bi[i:i+8],2)
        bitstr = chr(int(bi[i:i+8],2))
        text += bitstr
    return text

def bin_to_dna(bi):
    dna = ''
    for i in range(0,len(bi),2):
        key = bi[i:i+2]
        dna += bin_to_dna_table[key]
    return dna

def dna_to_bin(dna):
    bi = ''
    for n in dna:
        if n in ['A', 'T', 'C', 'G', 'a', 't', 'c', 'g']:
            bi += dna_to_bin_table[n.upper()]
    return bi
