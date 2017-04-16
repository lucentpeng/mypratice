#!/usr/bin/perl
#
# The traditional first program.

# Strict and warnings are recommended.
use strict;
use warnings;

my $mystring = "[2004/04/13] The date of this article.";
my $git_url = "http://twtpeunogit.deltaww.com:30000";
my $project = "project_ipcs.git";
my $branch = "master";
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

#Assign $1,$2 variable to other variable
my $link = $1;
my $port = $2;
print "The domain name is $link\n";
print "The port number is $port\n";

#Get current git project information
my $usr = `git config --global user.name`;
my $email = `git config --global user.email`;

#Remove any newline
$usr =~ s/\R//g;
$email =~ s/\R//g;


print "Current user name is $usr\n";
print "Current user email is $email\n";

my $push_url = "ssh\:\/\/$usr\\\@$link\:29418\/$project HEAD:refs\/for\/$branch";

print "gerrit push link is $push_url";
