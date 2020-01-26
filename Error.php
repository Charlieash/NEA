<!DOCTYPE html>
<html>
    <head>
        <title>Error</title>
    </head>
    <body style="background-color: rgb(69, 42, 69)">You have submitted an incorrect value 
        <h1 style ="font-size: 900%; text-align: right; "> Error</h1>
        <form method = "POST">
            <input type = submit name = return>
</form>
</body>
</html>
<?php
if(isset($_POST['return']))
{header("Location:Neawebpage.php");
}
