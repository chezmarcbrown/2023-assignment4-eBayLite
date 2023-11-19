document.addEventListener('DOMContentLoaded', function() {
    console.log('Auctions.js loaded successfully!');
    const watchlistIcon = document.getElementById('watchlist-icon');

    if (watchlistIcon) {
        watchlistIcon.addEventListener('click', function() {
            const listingId = this.dataset.listingId;

            // Check if the user is authenticated
            if (user.is_authenticated){
                // Send an AJAX request to toggle watchlist status
                fetch(`/toggle_watchlist/${listingId}/`)
                    .then(response => response.json())
                    .then(data => {
                        // Update the icon state
                        watchlistIcon.className = data.is_watchlisted ? 'on' : 'off';
                    })
                    .catch(error => console.error('Error:', error));
            }
        });
    }
});
