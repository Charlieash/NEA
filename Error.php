<!DOCTYPE html>
<html>
    <head>
        <title>Error</title>
    </head>
    <body style="background-color: rgb(69, 42, 69); font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif">
        <h1 style ="font-size: 900%; text-align: center; "> Error</h1>
        <h2 style = "font-size: 400%; text-align: center;">You have submitted an incorrect value </h2>
        <form method = "POST" style = "text-align:center;">
            <button class = "btn success" name = return style = "font-size: 220%;">Continue </button>
</form>
</body>
</html>
<?php
if(isset($_POST['return']))
{header("Location:Neawebpage.php");
}
