<?php
//echo "CICICICICIIC";

require_once('../../../wp-load.php');
require_once(ABSPATH . 'wp-admin/includes/user.php');


ini_set("log_errors", 1);
ini_set("error_log", "/tmp/php-error.log");
error_reporting(E_ALL);

error_log("AJAX.php");

if (!defined('ABSPATH')) {
    exit;
}

define('ACCESS_TOKEN', get_option('api_key'));
error_log(ACCESS_TOKEN);


//define('ACCESS_TOKEN', 'heaalhIoufLVHWgBEOCcLYRsCzxVlisN');

$arg0 = $_POST["arguments"][0];
$arg1 = $_POST["arguments"][1];
$arg2 = $_POST["arguments"][2];

function createConnection()
{

    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, 'https://demo-agent-cl.dizme.io/api/v1/connection/invitation');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, "{\"allow_multiple_read\":false,\"request_uid\":\""."diz_".uniqid()."\"}");
    //curl_setopt($ch, CURLOPT_POSTFIELDS, "{\"allow_multiple_read\":true,\"request_uid\":\""."diz_6070cc879a0f9\"}");
    
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

    $headers = array();
    $headers[] = 'Accept: application/json';
    $headers[] = 'x-auth-token: ' . ACCESS_TOKEN;
    $headers[] = 'x-dizme-agent-id: Araneum';
    $headers[] = 'Content-Type: application/json';
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    $result = curl_exec($ch);
    error_log("ciao");
    //var_dump ($result);
    if (curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
    }
    curl_close($ch);

    if (!empty(ACCESS_TOKEN)) {

        echo $result;
    } 
    else 
    {
        echo "Api key inesistentez";
    }
}


function getConnection($connectionId)
{

// cerca in tabella se la connessione  stata accettata!

$dblink = mysqli_connect("localhost","wordpress", "wordpress.007",  "wordpress");


/* If connection fails throw an error */

if (mysqli_connect_errno()) 
{
echo '{ "error": "no db"}';
}
else
{

$sqlquery = "SELECT * from dizme_connections where request_uid='".$connectionId."'";

error_log("SQL:".$sqlquery);

if ($result = mysqli_query($dblink, $sqlquery)) 
{

$status = "";
$connectionId = "";

    /* fetch associative array */

    while ($row = mysqli_fetch_assoc($result)) {

       $status =  $row["status"];
       $connectionId =  $row["connection_id"];
    }


// trovato, aggiorno?
    /* free result set */

    mysqli_free_result($result);

if ($status)
{

echo '{ "status": "'.$status.'",  "connectionId":  "'.$connectionId.'"}';

}
else
{
	echo '{ "status": "REQUESTED",  "connectionId":  ""}';
}


} // se risultato
} //se db

//echo "{ \"status\": \"ACTIVE\" }";

}

function offerCredential($identifier, $jsonObj)
{
	error_log("offerCredential");
    endsWith($identifier, 'ssi2') ? $ide = substr($identifier, 0, -1) : $ide = $identifier;
    $role = $jsonObj['role'];
    $connectionId = $jsonObj['connectionId'];
    $location = $jsonObj['email'];
    $name = $jsonObj['username'];
    $surname = $jsonObj['description'];
    //$definitionId = get_option('definitionId');
    
    error_log("offerCredential:".$connectionId);
    $definitionId = "WyHiuM9GK37w5tSSt5yChr:3:CL:102765:Employee";
    //$definitionId = "TxIDNkm6Gvyb5wCru52raJ8DkV:2:Employee:1.0";
	//$definitionId = "Nkm6Gvyb5wCru52raJ8DkV:2:Employee:1.0";
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://demo-agent-cl.dizme.io/api/v1/credential/offer');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1);
    
    //TODO QUERY MYSQL PER sapere il connection_id dal request_id
    
    
    $connection_id = getConnection2($connectionId);
    error_log("offerCredential:".$connection_id);
    //$connection_id = "d70daafa-afae-4989-b117-2cc5a5b04cc9";
    
    $parametri = "{\"request_uid\":\"$identifier\",\"connection_id\":\"$connection_id\",\"credential_def_id\":\"$definitionId\",\"credential_values\":[    {       \"name\": \"name\",       \"mime_type\": \"text/plain\",       \"value\": \"$name\"     }, {       \"name\": \"surname\",       \"mime_type\": \"text/plain\",       \"value\": \"$surname\"     },  {       \"name\": \"employee_number\",       \"mime_type\": \"text/plain\",       \"value\": \"$ide\"     }, {       \"name\": \"role\",       \"mime_type\": \"text/plain\",       \"value\": \"$role\"     },{       \"name\": \"location\",       \"mime_type\": \"text/plain\",       \"value\": \"$location\"     }, {       \"name\": \"company_name\",       \"mime_type\": \"text/plain\",       \"value\": \"Araneum Group srl\"     }],\"comment\":\"string\"}";
    
    
    //      {       \"name\": \"name\",       \"mime_type\": \"text/plain\",       \"value\": \"$name\"     }, {       \"name\": \"surname\",       \"mime_type\": \"text/plain\",       \"value\": \"$surname\"     },  {       \"name\": \"employee_number\",       \"mime_type\": \"text/plain\",       \"value\": \"$ide\"     }, {       \"name\": \"role\",       \"mime_type\": \"text/plain\",       \"value\": \"$role\"     },{       \"name\": \"location\",       \"mime_type\": \"text/plain\",       \"value\": \"location\"     }, {       \"name\": \"company_name\",       \"mime_type\": \"text/plain\",       \"value\": \"Araneum Group srl\"     }   
    
    
    
    error_log("PARAMETRI:".$parametri);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $parametri);
    
    
    //curl_setopt($ch, CURLOPT_POSTFIELDS, "{\"credentialValues\":{\"Identifier\":\"$ide\",\"Role\":\"$role\"},\"definitionId\":\"$definitionId\",\"connectionId\":\"$connectionId\",\"automaticIssuance\":true}");
    
    
    
    
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

    $headers = array();
    $headers[] = 'Accept: application/json';
    $headers[] = 'x-auth-token: ' . ACCESS_TOKEN;
    $headers[] = 'x-dizme-agent-id: Araneum';
    $headers[] = 'Content-Type: application/json';
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    $result = curl_exec($ch);
    
    error_log("RESULT:".$result);
    if (curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
    }
    curl_close($ch);
    

    if (!empty(ACCESS_TOKEN) || !empty($definitionId)) {
        echo $result;
    } else {
        echo "Api key inesistente3";
    }
}

function createUser($identifier, $jsonObj, $id)
{
	error_log("createUser:".$ide." ".$jsonObj['email']." ". $jsonObj['username']);
	
	if (!$jsonObj['email'])
		$email = $identifier."@ssi.it";
	else
		$email = $jsonObj['email'];

	if (!$jsonObj['username'])
		$username = $identifier;
	else
		$username = $jsonObj['username'];

		
	
    if (!empty(get_option($identifier . 'details'))) {
        update_option($identifier . 'details', $jsonObj);
    } else {
        add_option($identifier . 'details', $jsonObj);
    }
    $id == 0 ? $ide = $identifier : $ide = substr($identifier, 0, -1);
    echo $ide;
    $creds = array(
        'user_login' => $ide,
        'user_pass' => 'pippo',
        'user_email' => $email,
        'display_name' => $username,
        'role' => $jsonObj['role'],
    );
    wp_delete_user($id);
    delete_option($identifier . 'details');
    add_option($ide . 'details', $jsonObj);
    echo 'Ho Aggiunto un nuovo user con id: ' . wp_insert_user($creds);

}

function verifyCredential()
{
    $dt = new DateTime();
    $dt->setTimezone(new DateTimeZone('UTC'));
    $data = $dt->format('Y-m-d\TH:i:s\Z');
    
    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, 'https://demo-agent-cl.dizme.io/api/v1/verify/request');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);


    //curl_setopt($ch, CURLOPT_POSTFIELDS, "{\"attributes\":[{\"attributeNames\":[\"Identifier\",\"Role\"],\"policyName\":\"Credenziale\"}],\"revocationRequirement\":{\"validAt\":\"" . $data . "\"},\"name\":\"Credenziale\",\"version\":\"1.0.0\"}");


curl_setopt($ch, CURLOPT_POSTFIELDS, "{\"business_code\":\"CC1\",\"allow_multiple_read\":false,\"request_uid\":\""."diz_".uniqid()."\"}");

    $headers = array();
    $headers[] = 'Accept: application/json';
    $headers[] = 'x-auth-token: ' . ACCESS_TOKEN;
    $headers[] = 'x-dizme-agent-id: Araneum';
    $headers[] = 'Content-Type: application/json';
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    $result = curl_exec($ch);
    if (curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
        error_log('Error:' . curl_error($ch));
    }
    curl_close($ch);
    error_log("VERIFY:".$result);
    echo $result;
}

function getConnection2($request_id)
{

$connectionId = "";

error_log("getConnection2:".$request_id);

// cerca in tabella se la connessione  stata accettata!

$dblink = mysqli_connect("localhost","wordpress", "wordpress.007",  "wordpress");


/* If connection fails throw an error */

if (mysqli_connect_errno()) 
{
echo '{ "error": "no db"}';
}
else
{

$sqlquery = "SELECT connection_id from dizme_connections where request_uid='".$request_id."'";

error_log("SQL:".$sqlquery);

if ($result = mysqli_query($dblink, $sqlquery)) 
{


    /* fetch associative array */

    while ($row = mysqli_fetch_assoc($result)) {

       $connectionId =  $row["connection_id"];
    }


// trovato, aggiorno?
    /* free result set */

    mysqli_free_result($result);

	

} // se risultato
} //se db

return $connectionId;
}



function getVerifiedUser($request_id)
{

$connectionId = "";

error_log("getVerifiedUser:".$request_id);

// cerca in tabella se la connessione  stata accettata!

$dblink = mysqli_connect("localhost","wordpress", "wordpress.007",  "wordpress");


/* If connection fails throw an error */

if (mysqli_connect_errno()) 
{
echo '{ "error": "no db"}';
}
else
{

$sqlquery = "SELECT userid from dizme_verifications where request_uid='".$request_id."'";

error_log("SQL:".$sqlquery);

if ($result = mysqli_query($dblink, $sqlquery)) 
{


    /* fetch associative array */

    while ($row = mysqli_fetch_assoc($result)) {

       $connectionId =  $row["userid"];
    }


// trovato, aggiorno?
    /* free result set */

    mysqli_free_result($result);

	

} // se risultato
} //se db

return $connectionId;
}


function getVerification($verificationId,$request_uid)
{

error_log("getVerification:".$verificationId. " ". $request_uid);

/*
// cerca in tabella se la connessione  stata accettata!

$dblink = mysqli_connect("localhost","wordpress", "wordpress.007",  "wordpress");



if (mysqli_connect_errno()) 
{
echo '{ "error": "no db"}';
}
else
{

$sqlquery = "SELECT * from dizme_verifications where request_uid='".$connectionId."'";

error_log("SQL:".$sqlquery);

if ($result = mysqli_query($dblink, $sqlquery)) 
{

$status = "";
$connectionId = "";

 
    while ($row = mysqli_fetch_assoc($result)) {

       $status =  $row["status"];
       $connectionId =  $row["connection_id"];
    }


// trovato, aggiorno?
 
    mysqli_free_result($result);

if ($status)
{

echo '{ "state": "'.$status.'",  "connectionId":  "'.$connectionId.'"}';

}
else
{
	echo '{ "state": "REQUESTED",  "connectionId":  ""}';
}


} // se risultato
} //se db

//echo "{ \"status\": \"ACTIVE\" }";

*/

/*
    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, 'https://api.trinsic.id/credentials/v1/verifications/' . $verificationId);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'GET');
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);


    $headers = array();
    $headers[] = 'Accept: text/plain';
    $headers[] = 'Authorization: Bearer ' . ACCESS_TOKEN;
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    $result = curl_exec($ch);
    if (curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
    }
    curl_close($ch);
    */
    
    
    //echo $result;
    
    //echo "{ \"state\" : \"no\", \"isValid\" : 1 }";
    
    
    
    
    
    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, 'https://demo-agent-cl.dizme.io/api/v1/transaction/'.$verificationId.'/status');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'GET');
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);


    $headers = array();
    $headers[] = 'Accept: */*';
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    $result = curl_exec($ch);
    if (curl_errno($ch)) {
        echo '{ \"state\" : \"Error\",\"username\" : \"\", \"isValid\" : false }';
    }
    curl_close($ch);
    
    
    
    //echo $result;
    
    error_log("getVerification2".$result);
    $post = json_decode($result);

	if ($post->transaction_status=="SUCCESS")
		{
		
		// leggi username dalla tabella
		
		$username = getVerifiedUser($request_uid);
   		error_log("getVerification3".$username);
		
		echo "{ \"state\" : \"Accepted\",\"username\" : \"".$username."\", \"isValid\" : true }";
		}
	else

    echo "{ \"state\" : \" ".$post->transaction_status."  \", \"isValid\" : true }";

//    echo "{ \"state\" : \"Accepted\",\"username\" : \"dizme\", \"isValid\" : true }";
    
}

function authenticateUser($identifier)
{
    $result = wp_signon(array('user_login' => $identifier, 'user_password' => 'pippo', 'remember' => true));
    echo $identifier . " autenticato";
    error_log("authenticateUser".print_r($result,true));
}

function revokeCredential($identifier, $id)
{

// non faccio chiamate ma cancello solo l'utente
/*
    $ch = curl_init();
    $credentialId = get_option($identifier . 'details')['credentialId'];
    curl_setopt($ch, CURLOPT_URL, 'https://api.trinsic.id/credentials/v1/credentials/' . $credentialId);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'DELETE');
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);


    $headers = array();
    $headers[] = 'Authorization: Bearer ' . ACCESS_TOKEN;
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    $result = curl_exec($ch);
    if (curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
    }
    curl_close($ch);
    */
    wp_delete_user($id);
    delete_option($identifier . 'details');
    echo "OK";

}

function recuperaJSON($identifier)
{
    $lt = get_option($identifier . 'details');
    echo json_encode($lt);
}

switch ($_POST["functionname"]) {
    case 'createConnection':
        createConnection();
        break;
    case'offerCredential';
        offerCredential($arg0, $arg1);
        break;
    case 'createUser':
        createUser($arg0, $arg1, $arg2);
        break;
    case 'getConnection':
        getConnection($arg0);
        break;
    case 'verifyCredential':
        verifyCredential();
        break;
    case 'getVerification':
        getVerification($arg0, $arg1);
        break;
    case 'authenticateUser':
        authenticateUser($arg0);
        break;
    case 'revokeCredential':
        revokeCredential($arg0, $arg1);
        break;
    case 'recuperaJSON':
        recuperaJSON($arg0);
        break;
}


