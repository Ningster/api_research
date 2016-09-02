$(document).ready(function(){

  //input yelp category
  $("#get_fb_id_btn").click(function() {
    var category=document.getElementById('input_txt').value;
    $.ajax({
      url:"name_match_id/",
      type:"get",
      data:{"category":category},
      success:function(response){
        // console.log(response);
        // document.getElementById("fb_id_result").innerHTML = response['data'];
        $("#fb_id_result").append(
                       JSON.stringify(response['data'])
                     );
      },
    });
});


});
