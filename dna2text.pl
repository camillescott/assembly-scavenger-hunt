#!/usr/bin/perl -w
use strict;

#dna2text.pl
#Decode dna-encoded ascii text stored in a fasta file
#use 2-bit lookup table and descending-bit order encoding
#Preseve fasta format for learning purposes

#Jeremy Leipzig leipzig@gmail.com
#usage: perl dna2text,pl < dna.fa > text.txt

#http://www.aleph.se/Trans/Individual/Body/ascii.html
#A: 00 G: 01 C: 10 T: 11
my %lut = ( 'A' => '00', 'G' => '01', 'C' => '10', 'T' => '11' );
my $dna;

while (<>) {
    chomp;
    next if (/^$/);
    if (/>/) {
        if ( defined($dna) ) {
            print chooseOrt($dna) . "\n";
            $dna = '';
        }
        print $_. "\n";    #keep defline
    }
    else {
        $dna .= $_;
    }
}
print chooseOrt($dna) . "\n";

#print whichever orientation is wordier
sub chooseOrt {
    my $seq = shift;
    my $fwd = decode( dna2binary($seq) );
    my $rev = decode( dna2binary( RC($seq) ) );
    ( cmpWords( $fwd, $rev ) > 0 ) ? $fwd : $rev;
}

#convert dna into binary using lookup table
sub dna2binary {
    my $dna = shift;
    my $bin;
    foreach my $nt ( split( //, $dna ) ) {
        $bin .= $lut{$nt};
    }
    return $bin;
}

#pack binary into ascii
#look for ORFs
#http://mail.pm.org/pipermail/pikes-peak-pm/2004-April/000800.html
sub decode {
    my $bin  = shift;
    my $text = '';
    my $i    = 0;
    while ( $i <= length($bin) - 8 ) {
        my $sBin = substr( $bin, $i, 8 );
        my $l    = ( length $sBin );
        my $t    = pack "B$l", $sBin; #bit string (descending bit order inside each byte).
        if ( $t =~ /[\x20-\x7E]/ ) {    #printable characters
            $text .= $t;
            $i = $i + 8;
        }
        else {
            #if you get off an ORF then just skip that nucleotide/2bits
            $i = $i + 2;
        }
    }
    return $text;
}

#reverse complement
sub RC {
    my $seq = shift;
    my $rc  = reverse $seq;
    $rc =~ tr/ACGT/TGCA/;
    return $rc;
}

#compare two strings based on wordiness
#number of alphabetic characters
#number of common words - this should be internationalized
sub cmpWords {
    my ( $seq1, $seq2 ) = @_;
    my @m1;
    my @m2;
    return (
scalar( @m1 = $seq1 =~ /[A-Za-z]/g ) <=>
          scalar( @m2 = $seq2 =~ /[A-Za-z]/g )
||
        scalar( @m1   = $seq1 =~ /(the|of|to|and|a|in|is|it|you|that)/g ) <=>
          scalar( @m2 = $seq2 =~ /(the|of|to|and|a|in|is|it|you|that)/g )
    );
}
