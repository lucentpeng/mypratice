#!/usr/bin/perl
$file='file.txt';
open my $info, $file or die "Could not open $file: $!";

while( my $line = <$info>)  {   
    #execute command we would to do.
    print $line;    
    last if $. == 2;
}
close(INFO);


