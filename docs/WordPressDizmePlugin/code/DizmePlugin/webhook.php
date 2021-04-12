<?php
ini_set("log_errors", 1);
ini_set("error_log", "/tmp/php-error.log");
error_reporting(E_ALL);


error_log("WEBHOOK");

$input = file_get_contents('php://input');
$post = json_decode($input);
//file_put_contents(time()."-req.txt", print_r($post,true));


$connection_id = $post->connection_id;
$reused= $post->reused;
$status= $post->status;
$request_uid= $post->request_uid;

error_log("W1:". $connection_id. " " .$reused." ".$status." ".$request_uid);

$dblink = mysqli_connect("localhost","wordpress", "wordpress.007",  "wordpress");


/* If connection fails throw an error */

if (mysqli_connect_errno()) {

    error_log( "Could  not connect to database: Error: ".mysqli_connect_error());

    exit();
}

error_log( "C");
$sqlquery = "SELECT * from dizme_connections where request_uid='".$request_uid."'";

error_log($sqlquery);

if ($result = mysqli_query($dblink, $sqlquery)) {



/*
    $conto = 0;
    while ($row = mysqli_fetch_assoc($result)) {

       $conto =  $row["conto"];
    }
*/
	error_log("CONTO:".$conto);
	$conto = $result->num_rows;

// trovato, aggiorno?

	error_log("CONTO:".$conto);
	
    /* free result set */
    mysqli_free_result($result);

    if ($conto>0)
{

error_log(	 "esiste, aggiorno");
?>
{
  "status_code": "100",
  "message_code": "0",
  "message": "Success!"
}
<?php
}

else
{ // non trovato, inserisco

error_log( "inserisco");	
$sql      = "INSERT INTO dizme_connections(connection_id,status,request_uid,reused) VALUES (?, ?, ?, ?)";

/* Prepare statement */
$stmt     = $dblink->prepare($sql);

if(!$stmt) {

   echo 'Error: '.$dblink->error;
}
//echo "inserisco";	
 
/* Bind parameters */
$stmt->bind_param('ssss',$connection_id,$status,$request_uid,$reused);
 
//echo "inserisco";	
/* Execute statement */
$res = $stmt->execute();

//echo "inserisco";	
print_r($res,true);
 
//echo "inserito".$stmt->insert_id;

$stmt->close();
?>
{
  "status_code": "100",
  "message_code": "0",
  "message": "Success!"
}
<?php
}




}

/* close connection */

mysqli_close($dblink);

?>

