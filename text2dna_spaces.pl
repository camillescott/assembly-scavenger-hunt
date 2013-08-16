#!/usr/bin/perl -w

#text2dna.pl
#Encode ascii text as dna reads in a fasta format
#assume one read per line
#remove spaces before encoding

#Jeremy Leipzig leipzig@gmail.com
#usage: perl text2dna,pl < text.txt > dna.fa

#A: 00 G: 01 C: 10 T: 11
%lut = ( '00' => 'A', '01' => 'G', '10' => 'C', '11' => 'T' );
$readNum = 1;
while (<>) {
    chomp;
    next if (/^$/);
    print ">Seq_$readNum\n";
    print binary2dna(text2binary($_))."\n";
    $readNum++;
}

#convert binary into dna using lookup table
sub binary2dna {
    my $bin = shift;
    my $dna = '';
    for ( my $i = 0 ; $i <= length($bin)-2 ; $i += 2 ) {
        $dna .= $lut{ substr( $bin, $i, 2 ) };
    }
    return $dna;
}

#convert text into binary
#use descending-bit order encoding 
sub text2binary {
    my $text = shift;
    #http://mail.pm.org/pipermail/pikes-peak-pm/2004-April/000800.html
    my $l   = ( length $text ) * 8;
    return unpack "B$l", $text;
}
