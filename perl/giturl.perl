#!/usr/bin/perl
#
# The traditional first program.

# Strict and warnings are recommended.
use strict;
use warnings;

my $mystring = "[2004/04/13] The date of this article.";
my $git_url = "http://twtpeunogit.deltaww.com:30000";
#my $git_url = "http://twtpeunogit.deltaww.com:30000/p/project_ipcs.git";

if($mystring =~ m/(\d)/) {
	print "The first digit is $1.\n";
}

if($mystring =~ m/(\d+)/) {
		print "The first number is $1.\n";
	}

#if($git_url =~ m/http:\/\/([a-zA-Z0-9\.]+):(\d+)/) {
#	print "The url is http://$1.\n";
#	print "The port is $2.\n";
#}
$git_url =~ /http:\/\/([a-zA-Z0-9\.]+):(\d+)/;
print "The url is http://$1.\n";
print "The port is $2.\n";
