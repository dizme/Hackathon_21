<?php
ini_set("log_errors", 1);
ini_set("error_log", "/tmp/php-error.log");
error_reporting(E_ALL);

error_log("WEBHOOK-VERIFICA");

$input = file_get_contents('php://input');
$post = json_decode($input);
//file_put_contents(time()."-reqver.txt", print_r($input,true));


$connection_id = $post->connection_id;
$request_uid = $post->request_uid;
//$userid = $post->self_attested_attributes->role;
$userid = $post->revealed_attributes->employee_number;

error_log("W2:". $connection_id. " " .$reused." ".$status." ".$request_uid);
error_log("W2:". $userid. " " .$reused." ".$status." ".$request_uid);


function inserisci($request_uid,$userid)
{

$dblink = mysqli_connect("localhost","wordpress", "wordpress.007",  "wordpress");


/* If connection fails throw an error */

if (mysqli_connect_errno()) {

    error_log( "Could  not connect to database: Error: ".mysqli_connect_error());

    return false;
}

error_log( "inserisco");	
$sql      = "INSERT INTO dizme_verifications(request_uid,userid) VALUES ( ?, ?)";

/* Prepare statement */
$stmt     = $dblink->prepare($sql);

if(!$stmt) {

   error_log( 'Error: '.$dblink->error);
   return false;
}
//echo "inserisco";	
 
/* Bind parameters */
$stmt->bind_param('ss',$request_uid,$userid);
 
 error_log(print_r($stmt,true));
//echo "inserisco";	
/* Execute statement */
$res = $stmt->execute();
error_log(print_r($res,true));


//echo "inserisco";	
//print_r($res,true);
 
//echo "inserito".$stmt->insert_id;

$stmt->close();

/* close connection */

mysqli_close($dblink);
return true;
}


if (inserisci($request_uid,$userid))
{
error_log("OK");
?>
{
  "status_code": 100,
  "message_code": 0,
  "message": "Success!",
  "result": true,
  "send_response": true,
  "descriptions": [
    {
      "lang": "en",
      "message": "Verifica eseguita con successo"
    },
    {
      "lang": "it",
      "message": "Verify executed successfully"
    }
  ]
}
<?php
}
else
{
error_log("KO");
?>
{
  "status_code": 101,
  "message_code": 0,
  "message": "Errore!",
  "result": true,
  "send_response": true,
  "descriptions": [
    {
      "lang": "en",
      "message": "Verifica non eseguita con successo"
    },
    {
      "lang": "it",
      "message": "Verify NOT executed successfully"
    }
  ]
}
<?php
}

?>

