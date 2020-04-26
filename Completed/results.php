<!DOCTYPE html>
<html>
    <head>
        <title>GET A BUS</title>
    </head>
    <body style="background-color: rgb(69, 42, 69); font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif">
        <h1 style ="font-size: 500%; text-align: center; "> YOUR POSSIBLE BUSSES</h1>
        <p style = "font-size: 400%; text-align: center;"><?php $data = strval(file_get_contents('Backend\Data_Transfer\data.txt'));$place = ""; for($x = 0; $x < (strlen($data)); $x++){if($data[$x] != ","){$place = $place.$data[$x];} else{ echo($place.'<br>'); $place = "";}} ?>  </p>
        <form method = "POST" style = "text-align:center;">
            <button class = "btn success" name = return style = "font-size: 220%;">Continue </button>
        <form method = "POST" style = "text-align:center;">
            <button class = "btn success" name = graph style = "font-size: 220%;">Graph </button>
</form>
</body>
</html>
<?php
if(isset($_POST['return']))
{header("Location:Neawebpage.php");
}
if(isset($_POST['graph']))
{exec("Backend\graphing.py");
}
?>
