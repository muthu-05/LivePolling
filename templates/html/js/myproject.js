/*
This file contains all the custom code for ConnectMe and will be used for ajax calls
*/

$(document).ready(function() {

/* First Check for Page Auth, this will be the first function which will be executed  */

 $.ajaxSetup({
    headers: {
      'Authorization': "JWT " + $.cookie('token')
    }
 });

/* Call this function for validating token at server side to make sure that user is authenticated */
var ret_code=validateToken();

/* ############### Following Section Contains a code for Question Set and Quiz Generation ###################### */


/*###### Following section container code for user admin tables. Please check useradmin.html pages################  */

});



/* ########### Token Auth block begins here  #################### */

function validateToken()
{
if ( $.cookie('token') && $.cookie('username'))
  {
     var req1 = $.ajax({
        type: "GET",
        url: "/api/items",
    });
    req1.complete(chkResponse);
}
else
 {
  redirectLogin();
 }
}

function redirectLogin()
{
  alert("You have not logged in! please Signin");
  window.location.href = "login.html";
}

function chkResponse(response)
{
console.log(response);
if (response['status']==200 && response['statusText']=='OK')
 {
	  return 0;
 }
 else
  {
	redirectLogin();
  }
redirectLogin();
}

/* ########### Token Auth block end here  #################### */


function checkError(response) {
  var errordesc;
  var errorcode;

  if (response.responseJSON['description'])
  {
    errordesc = response.responseJSON['description'];
  }
  else
  {
    errordesc = "Unkown Error Occurred";
  }
  if (response.responseJSON['status_code'])
  {
    errorcode = response.responseJSON['status_code'];
  }
  else
  {
      errorcode = "Please try Again!";
  }

  alert("Login Failed :" + " " + errordesc + " - " + errorcode);
  deleteCookie();
  console.log(response);
}
