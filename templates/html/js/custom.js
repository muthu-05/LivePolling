/*
This file contains all the custom code for ConnectMe and will be used for ajax calls
*/
$(document).ready(function() {

if ( $.cookie('token') && $.cookie('username'))
  {
   console.log($.cookie('token'));
   console.log($.cookie('username'));
   $("#loginshow").hide();
   $("#loginhide").show();
   $("#uname").html(" " + $.cookie('username'));
  }
else
 {
  console.log($.cookie('username'));
  $("#loginshow").show();
  $("#loginhide").hide();
 }

$("#logout").click(function() {
deleteCookie();
window.location.href = "index.html";
});

  $.ajaxSetup({
    headers: {
      'Authorization': "JWT " + $.cookie('token')
    }
});

$("#tenancyform").submit(function(event) {
    /* stop form from submitting normally */
    event.preventDefault();
    var tenancy_req=$.ajax({
      type: "POST",
      url: "/api/tenancy",
      data: $('#tenancyform').serialize(),
    });
    tenancy_req.done(tenancySuccess);
    tenancy_req.fail(tenancyError);
  });


  /* Following function handles Jwt token access  */

  $("#loginform").submit(function(event) {
    /* stop form from submitting normally */
     event.preventDefault();
     var frmdata =  $('#loginform').serialize();
     var res = frmdata.split("=");
     passwd=res[2];
     var endloc = res[1].search( /&/i );
     var uname = res[1].substring(0, endloc);
     var __data = uname.replace(/%40/g, "@");
     uname = __data;
     console.log(uname);
     var str1 = '"{\\n\\\"username\\": \\"'+uname+'\\"'+', \\n\\"password\\": \\"'+passwd+'\\"\\n}"'
     console.log(str1);
     var req = $.ajax({
     type: "POST",
     url: "/auth",
     contentType: 'application/json',
     data: eval('"{\\n\\\"username\\": \\"'+uname+'\\"'+', \\n\\"password\\": \\"'+passwd+'\\"\\n}"')
     });
    req.done(getToken);
    req.done(getUsername(uname));
    req.fail(checkError);
    req.fail(deleteCookie);
    req.complete(checkLoggedIn);
   });
});



function twitterme() {
  alert("I am in twitterme");
}

function resetpassword() {
  alert("I am in resetpassword");
}


function registerme() {
  alert("I am in registerme");
}

function getToken(response)
{
  if (response['access_token'])
  {
  var jwt_token = response['access_token'];
  var token = jwt_token;
  console.log(token);
  $.cookie('token', token);
  console.log(response);
  }
}

function getUsername(uname)
{
  console.log(uname);
  $.cookie('username', uname);
}

function tenancySuccess(response){
  alert("Registeration Successfull!:");
  window.location.href = "login.html";
}

function tenancyError(response) {
  var desc;
  var retcode;

 console.log(response);
  alert("Registeration Failed:" + " " + desc + " - " + retcode);
  console.log(response);
  document.getElementById("tenancyform").reset();
}

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

  alert("Login Failed:" + " " + errordesc + " - " + errorcode);
  deleteCookie();
  console.log(response);
  document.getElementById("loginform").reset();
}

function checkLoggedIn()
{
if ($.cookie('token') && $.cookie('username'))
{
 $.ajaxSetup({
    headers: {
      'Authorization': "JWT " + $.cookie('token')
    }
  });
 uname = $.cookie('username');
 var req = $.ajax({
    type: "GET",
    url: "/api/usermgmt",
    dataType: "json",
    data:
    {
      "username": uname,
      "querytype": "cookie"
    }
 });
 req.done(setCookie);
 req.fail(checkError);
 req.complete(checkCookie);
 // alert("I am in Logged In");
 console.log(new Date());
  console.log('Processing Cookies');
  sleep(2000);
  console.log(new Date());
 window.location.href = "index.html";
 }
else
 {
  window.location.href = "login.html";
 }
}

function deleteCookie()
{
  var status = 1;
    if ($.cookie('token'))
      $.cookie("token", null, { path: '/' });
    if ($.cookie('username'))
      $.cookie("username", null, { path: '/' });
    if ($.cookie('firstname'))
        $.cookie("firstname", null, { path: '/' });
    if ($.cookie('lastname'))
        $.cookie("lastname", null, { path: '/' });
    if ($.cookie('designation'))
        $.cookie("designation", null, { path: '/' });
    if ($.cookie('tenancy_id'))
        $.cookie("tenancy_id", null, { path: '/' });
    if ($.cookie('role'))
        $.cookie("role", null, { path: '/' });
}

function setCookie(response)
{
console.log(response);
var firstname;
var lastname;
var role;
var designation;
var tenancy_id;
obj = JSON.parse(response);
// alert("I am inside setCookie1");
$.each(obj,function(i,item){
  firstname=item.first_name;
  lastname=item.last_name;
  role=item.role;
  designation=item.designation;
  tenancy_id=item.tenancy_id;
});

console.log(firstname + ' ' + lastname + ' ' + role + ' ' + designation + ' ' + tenancy_id)
$.cookie('firstname', firstname);
$.cookie('lastname', lastname);
$.cookie('designation', designation);
$.cookie('tenancy_id', tenancy_id);
$.cookie('role', role);
alert("Login Sucessfull!");
}

function checkCookie()
{
  var status = 1;
    if ($.cookie('token') && $.cookie('username') && $.cookie('firstname')  && $.cookie('lastname') && $.cookie('designation') && $.cookie('tenancy_id') && $.cookie('role')) {
      console.log('All the Cooikes are set')
  }
    else {
      deleteCookie();
      alert("Error Occurred in Login, Please try Again");
      window.location.href = "login.html";
    }
}

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}
