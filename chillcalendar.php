<?php

function clean($string) {
   
$string2 = preg_replace('/[^A-Za-z0-9\-.\/ ]/', '', $string); // Removes special chars.

return $string2;

}


if( $_POST["link"] ) {
$output = shell_exec(clean('/home/tull/opt/python-3.6.2/bin/python3 chillcalendar.py ' .  $_POST['link']));
echo "<a href='http://chillout.estamine.net/'>go back</a><br/><br/>";
echo "<a href='http://chillout.estamine.net/tourslist.xlsx'>link to tourslist excel file</a>";
echo "<br/><a href='http://chillout.estamine.net/calendar.html'>link to html calendar</a><br/>";

echo "<pre>" . $output . "</pre>";

exit();
 }
?>
<html>
 <body>
 
 <form action = "<?php $_PHP_SELF ?>" method = "POST">
 <br/><input type = "text" name = "link" value= "2018 4 Ana Luis Nuno Rafa Rafael Pedro Jose Gabi Miguel Ines" size="60"/>
  <br/><input type = "submit" />
 </form>
<br/>
 </body>
</html>
