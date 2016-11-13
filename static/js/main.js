function displayAll(){
    $("#edit_comment_button").on("click", function(){
        $(".edit_comment").css("opacity", "0.5")
    })







}


$(document).ready( displayAll )
$(document).on('page:load', displayAll)
