#!/usr/bin/perl
use strict;
use warnings;
use CGI qw/:standard/;
use CGI::Carp qw/ fatalsToBrowser warningsToBrowser/;
require '/home/bif724_161a18/public_html/Assignment1/tash_a1_lib.pl'; # subroutines containing html code


# subroutine grabs data from the html form
# validation();

if(param()) {
    # validates submitted form
    my $re1_id = param("re1_id");
    my $score = param("score");
    my $target_gene_id = param("target_id");
    my $re1_position = param("position");
    my $strand = param("strand");
    my $description = param("desc");
    my @error_mess; # stores error messages, if form filled out with incorrect data
    my $check_dups = 1; 
    my $dup_count = 0;
    my $sth;
    my @dups;
    
    # validates re1_id
    if ($re1_id !~ /(opossum|human|rat|xenopus|chicken)_42_(\d{1,2}[a-z]?)_((W|X|Y|Z)|1?[0-9]|2[0-3]|scaffold_\d{1,7})_(\d{1,9})_(r|f)/) {
        push @error_mess, "improperly formatted RE1 ID";  #[1-9]|[1-9][0-9]
        ## Also need to check for duplicates!
        $check_dups = 0; # set to 0 to prevent next if statement execution, if re1_id is invalid - there is no need
                         # to check whether it's in the table already!
    }
    
    # 
    if ($check_dups == 1) { # means re1_id entered is valid
        # password for making connection to mysql, stored as variable after calling subroutine
        my $password = get_paswd();
        # handle that makes connection to database or prints error message
        my $dbh =DBI->connect("DBI:mysql:host=db-mysql;database=bif724_161a18", "bif724_161a18", $password) or die "Problem connecting" . DBI->errstr;
        my $count = "select count(*) from a1_data where re1_id = ?"; # statement to see if it exists already
        $sth = $dbh->prepare($count) or die "problem with prepare in primary duplicate check" . DBI->errstr;
        $dup_count = $sth->execute($re1_id); # if it exists value will be 1 (defintely not 0)
        @dups = $sth->fetchrow_array;
        $dbh->disconnect() or die "Problem with disconnect" . DBI->errstr;
    }
       
    if ($dups[0] !=0) {
        push @error_mess, "this is a duplicate re1 id";  
    }
    
    # validates score value (must be greater than 0.9100 but less than 1 (to 4 decimal places))
    if ($score !~ /(1)|(0\.9[1-9]{1,3})/) {
        push @error_mess, "improperly formatted score value";
    }
    # validates target gene id
    if ($target_gene_id !~ /((ENS\w{3}G|ENSG)\d{11})/) {
        push @error_mess, "improperly formatted target gene id";
        ## Also need cross-checked
    }
    # validates position (better suited for a dropdown menu rather than textbox?)
    if ($re1_position !~ /(3'|5'|exon(\+)?|intron(\+)?)/i) {
        push @error_mess, "invalid position";
    }
    # validates strand value
    if ($strand !~ /(\+|\-)/) {
        push @error_mess, "invalid strand value";
    }
    # validates that no special characters are valid in description box
    ### produces internal server error when inserting into table and value is not null ###
    if ($description =~ /[\'\"\,\\\/]/g) {
        push @error_mess, "description contains invalid characters, please remove any ' \" , \ or / from text";
    }
    if (@error_mess) {
        print "Content-type: text/html\n\n";
        # makes new tab heading, includes css file
        print begin_html("Upload a File - Upload Error!", "tash_a1_upload.css");
        foreach (@error_mess) {
            print "<div class='error'><font color='#670046'>error: $_<br></div>";
        }
        print &form();
    }
}

else {
    # form not submitted, so display form
    print "Content-type: text/html\n\n";
    print begin_html("Upload a File", "tash_a1_upload.css");
    print &form();
}

print end_html();



sub form() {
    my $file_name = param('upload_file');
    my $upload_fh = upload('upload_file');
    
    return<<FORM;
    
    <form action=$0" method="post" enctype="multipart/form-data">
    <label class="upload"><input type="file" name="upload_file"><br/></label>
    <input type="submit"><input type ="reset">
    </form>
    
FORM

}
