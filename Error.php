<!DOCTYPE html>
<html>
    <head>
        <title>Error</title>
    </head>
    <body style="background-color: rgb(69, 42, 69)">
        <h1 style ="font-size: 900%; text-align: center; "> Error</h1>
        <h2 style = "font-size: 400%; text-align: center;">You have submitted an incorrect value </h2>
        <form method = "POST" style = "text-align:center; font-size: 600%">
            <button class = "btn success" name = return >Continue </button>
</form>
</body>
</html>
<?php
if(isset($_POST['return']))
{header("Location:Neawebpage.php");
}
