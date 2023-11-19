document.addEventListener('DOMContentLoaded', function() {
    console.log('Auctions.js loaded successfully!'); // to debug
    const watchlistIcon = document.getElementById('watchlist-icon');

    if (watchlistIcon) {
        watchlistIcon.addEventListener('click', function() {
            const listingId = this.dataset.listingId;

            // Check if the user is authenticated
            if (user.is_authenticated){
                // Toggle the heart icon class
                //this.classList.toggle('fas');
                //this.classList.toggle('far');

                // Send an AJAX request to toggle watchlist status
                //fetch(`/toggle_watchlist/${listingId}/`) // ---- this one is using previous 'toggle_watchlist' view ---
                fetch("api/status")
                    .then(response => response.json())
                    .then(data => {
                        // Update the icon state

                        //this.classList.toggle('fas', data.is_watchlisted);
                        //this.classList.toggle('far', !data.is_watchlisted);
                        watchlistIcon.className = data.is_watchlisted ? 'on' : 'off';
                        watchlistIcon.innerHTML = data.is_watchlisted ? 'Watchlisted' : 'Not Watchlisted';
                    })
                    .catch(error => console.error('Error:', error));
            }
        });
    }
});
