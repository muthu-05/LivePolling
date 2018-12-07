/*
This file contains all the custom code for ConnectMe and will be used for ajax calls
*/

var usertable1;
var QsetTable1;
$(document).ready(function() {

/* First Check for Page Auth, this will be the first function which will be executed  */

 $.ajaxSetup({
    headers: {
      'Authorization': "JWT " + $.cookie('token')
    }
 });

/* Call this function for validating token at server side to make sure that user is authenticated */
var ret_code=validateToken();


$("#useradmintab1").hide();

/* ### Admin block for user administration will be enabled if and only if current role of the user is admin */

if ($.cookie('role') == 'ADMIN')
{
$("#useradmintab1").show();
$("#adduser1").hide();
$("#adduserbtn1").hide();
$("#showuserreportbtn1").hide();
populateTabData();

$("#showuserreportbtn1").click(function() {
  showuserreportbtn1();
  populateTabData();
});

$("#useradmintab1").click(function() {
  populateTabData();
  useradmintab1();
});

$("#popadduserfrm1").click(function() {
   popadduserfrm1();
});

$("#adduser1").submit(function(event) {
    /* stop form from submitting normally */
    event.preventDefault();
    var data = $('#adduser1').serializeArray();
    console.log(data);
    var tenancy_id = $.cookie('tenancy_id');
    data.push({name: "tenancy_id", value: tenancy_id})
    console.log(data);
    var req=$.ajax({
      type: "POST",
      url: "/api/usermgmt",
      data: $.param(data),
    });
    req.done();
    req.fail();
    req.complete(resetAdduser1Form);
 });
}
else {
  $("#adduser1").hide();
  $("#adduserbtn1").hide();
  $("#showuserreportbtn1").hide();
  $("#listuserdata1").hide();
  $("#popadduserfrm1").hide();
  $("#useradmintab1").hide();
}
/* ##### ADMIn Role Check Ends here ######## */

$('#userreport1').on( 'click', '#editubtn', function () {
        var data=usertable1.row( $(this).parents('tr') ).data();
        //populateuserform();
} );

/*###### The above section contain code for user admin tables. Please check useradmin.html pages. The above code section ends here ################  */

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


/* ############ User Admin Table Management begin here ############## */

function populateTabData()
{
 var tenancy_id = $.cookie('tenancy_id');
 console.log('tenancy_id');

 var req = $.ajax({
    type: "GET",
    url: "/api/usermgmt",
    dataType: "json",
    data:
    {
      "tenancy_id": tenancy_id,
      "querytype": "userreport"
    }
 });
 req.done(buildTable);
 req.fail(checkError);
}

function buildTable(response)
{
  console.log(response);
  obj = JSON.parse(response);
  var rowdata;
  console.log(obj);

var resultarr= [];

obj.forEach(function(Object){
    resultarr.push([Object.first_name,Object.last_name,Object.email_id,Object.role,Object.designation,Object.mobile_num,Object.user_uid]);
});

console.log(resultarr);

usertable1= $('#userreport1').DataTable( {
        destroy: true,
        data: resultarr,
        columns: [
            { title: "FirstName" },
            { title: "LastName" },
            { title: "Address" },
            { title: "Role" },
            { title: "Designation" },
            { title: "Mobile Num" },
            { title: "Edit" },            
           ],
            "columnDefs": [ {
   	        "targets": [6],
        	"data": null,
	        "defaultContent": "<button id='editubtn'>Edit!</button>" + "<button id='deleteubtn'>Delete!</button>"
                       } ],
    } );

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

  alert("Login Failed :" + " " + errordesc + " - " + errorcode);
  deleteCookie();
  console.log(response);
}

function populateuserform (frm,data)
{
$.each(data, function(key, value){  
    var $ctrl = $('[name='+key+']', frm); 
    if($ctrl.is('select')){
        $("option",$ctrl).each(function(){
            if (this.value==value) { this.selected=true; }
        });
    }
    else {
        switch($ctrl.attr("type"))  
        {  
            case "text" :   case "hidden":  case "textarea":  
                $ctrl.val(value);   
                break;   
            case "radio" : case "checkbox":   
                $ctrl.each(function(){
                   if($(this).attr('value') == value) {  $(this).attr("checked",value); } });   
                break;
        } 
    } 
});  

}

function resetAdduser1Form()
{
$("#adduser1").trigger("reset");
}

function showuserreportbtn1()
{
  $("#listuserdata1").show();
  $("#adduser1").hide();
  $("#adduserbtn1").hide();
  $("#showuserreportbtn1").hide();
  $("#popadduserfrm1").show();
  $("#userreport1").show();
}

function useradmintab1()
{
  $("#listuserdata1").show();
  $("#adduser1").hide();
  $("#adduserbtn1").hide();
  $("#showuserreportbtn1").hide();
  $("#popadduserfrm1").show();
}

function popadduserfrm1 ()
{
  $("#adduser1").show();
  $("#adduserbtn1").show();
  $("#showuserreportbtn1").show();
  $("#listuserdata1").hide();
  $("#popadduserfrm1").hide();
  $("#userreport1").hide();
}
/* ############ User Admin Table Management end here ########### */
