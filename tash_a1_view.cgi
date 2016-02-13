#!/usr/bin/perl
use strict;
use warnings;
use DBI;
require '/home/bif724_161a18/.secret';
require '/home/bif724_161a18/public_html/Assignment1/tash_a1_lib.pl';
print "Content-type: text/html\n\n";

my $password = get_paswd();

# handle that connects to database, displays error if connection cannot be made
my $dbh =DBI->connect("DBI:mysql:host=db-mysql;database=bif724_161a18", "bif724_161a18", $password) or die "Problem connecting" . DBI->errstr;
# form query
my $sql = "select * from a1_data";
# prepares query
my $sth = $dbh->prepare($sql) or die "Problem with prepare" . DBI->errstr;
# executes query
my $new_data = $sth->execute() or die "Problem with execute" . DBI->errstr;

print begin_html("View All Records","tash_a1_view.css");
print <<T_HEADER;
    <table class ="view">
   
            <tr><th><a href="#">RE1 ID</a></th><th><a href="#">Score</a></th><th><a href="#">Target Gene ID</a></th><th>RE1 Position</th><th>Sense</th><th>Description</th></tr>
T_HEADER



if ($new_data != 0) {
      
      # loops through if there is data
      while (my @row = $sth->fetchrow_array) {
        print "<div class ='test'><tr><td>$row[0]</td><td>$row[1]</td><td>$row[2]</td><td>$row[3]</td><td>$row[4]</td><td>$row[5]</td></tr></div>";
      }
      
} else {
      # message prints if no data is found, ie $new_data = 0
    print "<tr colspan='3'><td>no records found</td></tr>";
}
# release db connection and use or die in case of errors
$dbh->disconnect() or die "Problem with disconnect" . DBI->errstr;

print "</table>";

print end_html();
