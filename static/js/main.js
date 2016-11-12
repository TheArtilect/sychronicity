function displayAll(){
    url = window.location.href;

    function reloadPage(){
        window.location.replace(url)
    }

    $(".refresh").on('click', function(){
        reloadPage()

    })






}


$(document).ready( displayAll )
$(document).on('page:load', displayAll)
