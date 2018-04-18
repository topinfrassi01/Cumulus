$(document).ready(function(){
    $('.keyword-link').click(function(e){
        e.preventDefault();

        query_string = JSON.stringify($('.keyword-articles', $(this)).val());
        
        request = $(this).attr('href') +  '/ids='+ query_string;
        window.location.href = request;
    });
});