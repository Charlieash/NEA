<!DOCTYPE html>
<html>
    <head>
        <title>Result</title>
    </head>
    <body style="background-color: rgb(69, 42, 69); font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif">
        <h1 style ="font-size: 500%; text-align: center; "> YOUR POSSIBLE BUSSES</h1>
        <p style = "font-size: 400%; text-align: center;"><?php $data = file_get_contents('data.txt');$a = 0; $b = 8;for($x = 0; $x <= (strlen($data)/8)-1; $x++){ echo(substr($data,$a, $b)."<br>"); $a =$a + 8; $b=$b+8;} ?>  </p>
        <form method = "POST" style = "text-align:center;">
            <button class = "btn success" name = return style = "font-size: 220%;">Continue </button>
</form>
</body>
</html>
<?php
if(isset($_POST['return']))
{header("Location:Neawebpage.php");
}
?>