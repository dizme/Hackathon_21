let offerUrl;
const urlAjax = 'ajax.php';
let verificationRequestUrl;
let verificationId;
let isValid;

function createConnection_con_div() {
    let isSubscriber;
    let identifier;
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const role = document.getElementById('role').value;
    const description = document.getElementById('description').value;

    let jsonObj = {
        username: username,
        email: email,
        role: role,
        description: description,
    };

    role === 'subscriber' ? isSubscriber = true : isSubscriber = false;
    isSubscriber ? identifier = guid() + 'ssi' : identifier = guid() + 'ssi2';
    console.log(username + ' ' + email + ' ' + role + ' ' + description);

//$("#div_widget").show();
                


    
}


function createConnection() {
    let isSubscriber;
    let identifier;
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const role = document.getElementById('role').value;
    const description = document.getElementById('description').value;

    let jsonObj = {
        username: username,
        email: email,
        role: role,
        description: description,
    };

    role === 'subscriber' ? isSubscriber = true : isSubscriber = false;
    isSubscriber ? identifier = guid() + 'ssi' : identifier = guid() + 'ssi2';
    console.log(username + ' ' + email + ' ' + role + ' ' + description);

    $.ajax({
        url: urlAjax,
        type: 'POST',
        data: {functionname: 'createConnection', arguments: [],},
        success: function (result) {
            try {
            	console.log("result:"+result);
            	//alert(result);
                const jsonResult = JSON.parse(result);
                const connectionId = jsonResult['request_uid'];
                const invitationUrl = jsonResult['invitation_short_link'];
                console.log('Invitation URL :' + invitationUrl);
                $(".qrcode").attr("src", "https://chart.googleapis.com/chart?cht=qr&chs=200x200&chl=" + invitationUrl);
                $(".qrcode").show();
                jsonObj = Object.assign({connectionId: connectionId}, jsonObj);
                pollingReg(identifier, connectionId, isSubscriber, jsonObj);
            } catch (e) {
                console.log(e);
                $(".testo").text('Api key inesistenteA');
                $(".testo").css('color', 'red');
            }
        },
    });
}

function pollingReg(identifier, connectionId, isSubscriber, jsonObj) {
    let state;
    let refreshId = setInterval(function () {
        $.ajax({
            url: urlAjax,
            type: 'POST',
            data: {functionname: 'getConnection', arguments: [connectionId],},
            success: function (result) {
            	console.log(result);
                
                const jsonResult = JSON.parse(result);
                status = jsonResult['status'];
                //connectionId = jsonResult['connectionId'];

            },
            complete: function () {
                console.log(status);
                if (status === "ACTIVE") {
                	console.log("identifier:"+identifier)
                    if (isSubscriber)
                        offerCredential(identifier, jsonObj);
                     createUser(identifier, jsonObj,);
                    clearInterval(refreshId);
                }
            }
        });

    }, 10000);
}

function offerCredential(identifier, jsonObj) {
    let credentialId;
    
    console.log("offerCredential");
    console.log(identifier);
    console.log(jsonObj);
    $.ajax({
        url: urlAjax,
        type: 'POST',
        data: {functionname: 'offerCredential', arguments: [identifier, jsonObj],},
        success: function (result) {
            const jsonResult = JSON.parse(result);
            credentialId = jsonResult['credentialId'];
        },
        complete: function () {
            jsonObj = Object.assign({credentialId: credentialId}, jsonObj);
        },
    });
}

function createUser(identifier, jsonObj, id=0) {
    $.ajax({
        url: urlAjax,
        type: 'POST',
        data: {functionname: 'createUser', arguments: [identifier, jsonObj, id],},
        complete: function (result) {
            console.log(result);
            console.log("OK CREATO");
            console.log(jsonObj);
            $(".testo").text('Utente creato! Attendere Approvazione!');
                $(".testo").css('color', 'green');
        },
    });
}

function authenticateUser() {
	console.log("authenticateUser");
    $(".form").hide();
    $.ajax({
        url: urlAjax,
        type: 'POST',
        data: {functionname: 'verifyCredential', arguments: [],},
        success: function (result) {
            try {
                console.log(result);
                let jsonResult = JSON.parse(result);
                verificationRequestUrl = jsonResult['invitation_short_link'];
                verificationId = jsonResult['tid'];
                request_uid = jsonResult['request_uid'];
                console.log(verificationRequestUrl);
                console.log(verificationId);
                $(".qrcode").attr("src", "https://chart.googleapis.com/chart?cht=qr&chs=200x200&chl=" + verificationRequestUrl);
                $(".qrcode").show();
                pollingAuth(verificationId, request_uid);
            } catch (e) {
            	console.log(e);
                $(".testo").text('Api key inesistenteB');
                $(".testo").css('color', 'red');
            }
        }
        ,
    });
}

function pollingAuth(verificationId, request_uid) {
    let refreshId = setInterval(function () {
        $.ajax({
            url: urlAjax,
            type: 'POST',
            data: {functionname: 'getVerification', arguments: [verificationId,request_uid],},
            success: function (result) {
                jsonResult = JSON.parse(result);
                state = jsonResult['state'];
                isValid = jsonResult['isValid'];
                identifier = jsonResult['username'];
                console.log("state:"+state+ " isValid:"+isValid+ " username:"+identifier);
                
            },
        });
        if (state === "Accepted" && isValid === true) {
            console.log(state);
            //identifier = jsonResult['proof']['Credenziale']['attributes']['Identifier'];
            
            //identifier = "";
            
            $.ajax({
                url: urlAjax,
                type: 'POST',
                data: {functionname: 'authenticateUser', arguments: [identifier],},
                success: function (result) {
                    console.log(result);
                    $(".qrcode").hide();
                    $(".testo").text('Utente autenticato');
                },
            });
            clearInterval(refreshId);
        } else if (state === "Accepted" && isValid === false) {
            $(".testo").text('Credenziale non valida');
            $(".testo").css('color', 'red');
            $(".qrcode").hide();
            console.log("Credenziale non valida");
            clearInterval(refreshId);
        }
    }, 5000);
}


function guid() {
    let s4 = () => {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    }
    return s4() + s4() + s4();
}

function showForm() {
    $(".form").show();
}
