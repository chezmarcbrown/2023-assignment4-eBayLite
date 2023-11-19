$(document).ready(function() {
    var csrfToken = $('#csrfToken').val(); // Assuming CSRF token is in a hidden field with ID 'csrfToken'

    $('.watchlist-icon').click(function() {
        console.log("Icon clicked, auction ID: ", $(this).data('listing-id'));
        var auctionId = $(this).data('listing-id');
        var icon = $(this); // Cache the icon element for use in the callback

        // AJAX call to toggle watchlist
        $.ajax({
            url: '/watchlist/' + auctionId, 
            method: 'POST',
            data: {
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                // Toggle icon class based on response
                if (response.added) {
                    icon.removeClass('fa-regular').addClass('fa-solid');
                } else {
                    icon.removeClass('fa-solid').addClass('fa-regular');
                }
            },
            error: function() {
                console.error('Error toggling watchlist item.');
            }
        });
    });
});
