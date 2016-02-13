#!/usr/bin/perl
use strict;
use warnings;
use CGI qw/:standard/;
use CGI::Carp qw/ fatalsToBrowser warningsToBrowser/;
use DBI;
require '/home/bif724_161a18/public_html/Assignment1/tash_a1_lib.pl'; # subroutines containing html code
require '/home/bif724_161a18/.secret';

my $password = get_paswd();


if(param()) {
    # validates submitted form
    my $re1_id = param("re1_id");
    my $score = param("score");
    my $target_gene_id = param("target_id");
    my $re1_position = param("position");
    my $strand = param("strand");
    my $description = param("description");
    my @error_mess; # stores error messages, if form filled out with incorrect data
    
    if ($re1_id !~ /(opossum|human|rat|xenopus|chicken)_42_(\d{1,2}[a-z]?)_(W|X|Y|Z|1?[0-9]|2[0-3]|scaffold_\d{1,7})_(\d{1,9})_(r|f)/) {
        push @error_mess, "improperly formatted RE1 ID";
        ## Also need to check for duplicates!
    }
    if ($score !~ /(1)|(0\.9[1-9]{1,3})/) {
        push @error_mess, "improperly formatted score value";
    }
    if ($target_gene_id !~ /((ENS\w{3}G|ENSG)\d{11})/) {
        push @error_mess, "improperly formatted target gene id";
        ## Also need cross-checked
    }
    if ($re1_position !~ /(3'|5'|exon(\+)?|intron(\+)?)/i) {
        push @error_mess, "invalid position";
    }
    if ($strand !~ /(\+|\-)/) {
        push @error_mess, "invalid strand value";
    }
    if ($description =~ /[\'\"\,\\\/]/g) {
        push @error_mess, "description contains invalid characters, please remove any ' \" , \ or / from text";
    }
    if (@error_mess) {
        print "Content-type: text/html\n\n";
        print begin_html("Add a Record - Entry Error!", "tash_a1_add.css");
        foreach (@error_mess) {
            print "<div class='relative'>$_<br></div>";
        }
        print form();
    }

    
    else {

        my $dbh =DBI->connect("DBI:mysql:host=db-mysql;database=bif724_161a18", "bif724_161a18", $password) or die "Problem connecting" . DBI->errstr;
        # command for sql
        my $sql = "insert into a1_data values (?,?,?,?,?,?)";
        # prepares command
        my $sth = $dbh->prepare($sql) or die "problem with prepare" . DBI->errstr;
        my $rows = $sth->execute($re1_id,$score,$target_gene_id,$re1_position,$strand,$description);
        
        if ($rows == 1) {
            print "Location: http://zenit.senecac.on.ca/~bif724_161a18/Assignment1/tash_a1_view.cgi\n\n";
            
        } else {
            print "couldn't insert data\n";
        }
        # drops connection to database and displays error if problem
        $dbh->disconnect() or die "Problem with disconnect" . DBI->errstr;
    }   
}

else {
    # form not submitted, so display form
    print "Content-type: text/html\n\n";
    print begin_html("Add a Record", "tash_a1_add.css");
    print form();
}

print end_html();

sub form {
    my $re1_id = param('re1_id');
    my $score = param('score');
    my $target_gene_id = param('target_id');
    my $position = param('position');
    my $strand = param('strand');
    my $positive = $strand eq '+'?"checked":"";
    my $negative = $strand eq '-'?"checked":"";
    my $description = param('descr');
    
    return<<FORM
    <form action="$0" method="post">
    <div class="table">
    <table class="add">
        <tr><td>RE1 ID</td><td><input type ="text" class="textbox" name ="re1_id" placeholder="e.g. rat_42_34l_1_41581388_f" value = "$re1_id"</td></tr>
        <tr><td>Score</td><td><input type ="text" class="textbox" name ="score" placeholder="e.g. > 0.9100 but < 1" value = "$score"</td></tr>
        <tr><td>Target Gene ID</td><td><input type ="text" class="textbox" name ="target_id" placeholder="e.g. ENSG00000204624" value ="$target_gene_id"</td></tr>
        <tr><td>Position</td><td><input type ="text" class="textbox" name ="position" placeholder="e.g. EXON or 3' etc." value = "$position"</td></tr>
        <tr><td>Strand</td><td>
                    positive <input type ="radio" name ="strand" value = "+" $positive>       
                    negative <input type ="radio" name ="strand" value = "-" $negative></tr></td>
        <tr><td>Description</td><td>
            <textarea name ="descr" class="textbox" placeholder="Enter in a description, if available">$description</textarea>
        </td></tr>
        <tr><td></td><td colspan = "2" align = "right"><input type ="submit"></td></tr>  
    </table>
    </div>
    </form>
FORM

}



    

