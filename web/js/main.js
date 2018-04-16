function get_keywords(callback) {
    $.get("http://localhost:5000/", null, callback)
}

$(document).ready(function(){
    var words_container = $('.words-container');
    
    get_keywords(function(data) {
        for(var row in data) {
            console.log(row);
        }
    });
});