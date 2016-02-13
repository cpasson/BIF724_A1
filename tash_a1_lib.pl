sub begin_html {
    my $tabHeading = shift;
    my $css_file = shift;
    return<<begin_html;
<!DOCTYPE html>
<html>
    <head>
        <title>$tabHeading</title>
        <link rel="stylesheet" href="$css_file">
    </head>
    <body>
    <div class="jumbotron">
        <div class="nameheader">
            <h1 style="text-align:center;">RE1 TARGET GENE DATA</h1>
        </div>
        <div class="nav">
            <div class="container">
                <ul class="pull-left">
                    <li><a href="http://zenit.senecac.on.ca/~bif724_161a18/Assignment1/tash_a1_add.cgi">Add a Record</a></li>
                    <li><a href="http://zenit.senecac.on.ca/~bif724_161a18/Assignment1/tash_a1_view.cgi">View All Records</a></li>
                    <li><a href="#">Upload a File</a></li> 
                </ul>
            </div>
        </div>
  
  


begin_html
}
sub end_html {
    return<<end_html;
    </div>
    </body>
</html>
end_html
}
1;

