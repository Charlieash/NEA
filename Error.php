<!DOCTYPE html>
<html>
    <head>
        <title>Error</title>
    </head>
    <body style="background-color: rgb(69, 42, 69)">
        <h1 style ="font-size: 900%; text-align: left; "> Error</h1>
        <form method = "POST">
            <input type = submit name = return>
</form>
You have submitted an incorrect value </body>
</html>
<?php
if(isset($_POST['return']))
{header("Location:Neawebpage.php");
}
