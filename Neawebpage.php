<!DOCTYPE html>
<html>
    <head>
        <title>GET A BUS</title>
    </head>
    <body style="background-color: rgb(69, 42, 69)">
        <h1 style ="font-size: 900%; text-align: center; "> GET A BUS</h1>
        <form  method = "POST" style ="text-align: center; font-size: 200%; font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif" size="300">
        Starting Location: <input name = "data" list="Bus Stops">
            <br></br> 
        Ending Location: <input  name = "data2" list="Bus Stops">
            <br></br>
        Time: <input name = "data3" type = text>
        <br></br> 
            <input type = submit> 
            <datalist id="Bus Stops">
              <option value="Guildford Station">
              <option value="Shalford">
              <option value="High Path Road">
              <option value="Merrow Chruch">
              <option value="Bramley">
            </datalist>
          </form>
    </body>
</html>

<?php
  if(isset($_POST['data']))
  {
  $data=$_POST['data']."\r\n";
  $fp = fopen('data.txt', 'w');
  fwrite($fp, $data);
  fclose($fp);
  }
  if(isset($_POST['data2']))
  {
  $data=$_POST['data2']."\r\n";
  $fp = fopen('data.txt', 'a');
  fwrite($fp, $data);
  fclose($fp);
  }
  if(isset($_POST['data3']))
  {
  $data=$_POST['data3']."\r\n";
  $fp = fopen('data.txt', 'a');
  fwrite($fp, $data);
  fclose($fp);
  exec("NEA.py");
  }
  ?>