$(document).ready(function(){
  var user_access_token = null;
  $("#get_fb_id_btn").click(function() {
    // FB.api("/ME", "GET", {access_token:"EAACEdEose0cBAE8yjzTgDc88YKCONPAYHZBytTIlyywkKgZAVaUISbX75iZBxj0poBECDgNwoNO0QwSv24eE3QXbZAfz1htN2b5hwy6NuJ3ZCkR3VQVXTxg90oZBPleeDDFeYCJo2Sha6g4a7gFqyiZBrIJ1LHG1rbUb6wLi2G1UlQNzvjA3ZBMD36Qo1HVU8L0ZD"},
    // function(res){
    //   console.log(res);
    // });
    // FB.api('/oauth/access_token','GET',
    //     {client_id:'1804960436416588', client_secret:'89c50ed3bf7c24be74b90c4f9cb4dbe1',grant_type:'client_credentials'},
    //     function(response) {
    //         console.log(response);
    //     });
    // FB.api('/microsoft','GET',
    //     {access_token:"1804960436416588|b8AnZIENweUP-yytnzWwqJZtuj4"},
    //     function(response) {
    //         console.log(response);
    //     });
      FB.login(function(response) {
          if (response.authResponse) {
           user_access_token=FB.getAuthResponse().accessToken;
           console.log(user_access_token);
           console.log('Welcome!  Fetching your information.... ');
           FB.api('/me', function(response) {
             console.log('Good to see you, ' + response.name + '.');
             console.log(encodeURIComponent('22Café-22號咖啡館-772892866054564'));
           });
           FB.api('/772892866054564/likes','GET',
               {"access_token":user_access_token,"summary":true},
               function(response) {
                 alert(response['data'].length);
                  //  $("#msft_result").append(
                  //    JSON.stringify(response)
                  //  );
               });
          } else {
           console.log('User cancelled login or did not fully authorize.');
          }
      });
});


});
