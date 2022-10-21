$(function() {
    const searchForm = $('#searchForm');

    $("#log_level").change(function() {
        searchForm.submit();
    });

    $("#logger_name").change(function() {
        searchForm.submit();
    });

    $("#search_text").keyup(function(event) {
        // When press enter key
        if (event.keyCode === 13) {
            searchForm.submit();
        }
    });

})
