<?php
$id=trim($_POST["id"]);
$Name=trim($_POST["Name"]);
$cover=trim($_POST["cover"]);

$servername="localhost";
$username="root";
$password="12345678";
$dbname="manga";
// create connection
$conn=mysqli_connect($servername,$username,$password,$dbname);
if(!$conn){
    die("Connection failed ".mysqli_connect_error());
}
$sql="INSERT INTO `anime` (`id`, `Name`, `cover`) VALUES ('$id', '$Name', '$cover')";
//echo $sql."<br>";
$result=mysqli_query($conn,$sql);
if($result){
    echo "<h1>Insert new record</h1>";
    echo "<h1>successfully!</h1>";
    echo "<button><a href='index.php' style='text-decoration: none'>Back</a></button>";
}
else echo "Error: ".$sql."<br>".mysqli_error($conn);
mysqli_close($conn);
?>