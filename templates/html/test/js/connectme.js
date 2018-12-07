/*global jQuery:false */
jQuery(document).ready(function($) {
    $(#tenancy-button).click(initTenant);
    alert("I am in a function");
  });

function initTenant() {
 $.ajax({url: "index.html",
         data: $("#signupform").serialize(),
         sucess: showAlert 
         error: alert("Error Ocurred") });
}

function testFunction() {
    alert("Test");
}
