document.addEventListener('DOMContentLoaded', function() {
    console.log('Auctions.js loaded successfully!'); // to debug
    const watchlistIcon = document.getElementById('watchlist-icon');

    if (watchlistIcon) {
        watchlistIcon.addEventListener('click', function() {
            const listingId = this.dataset.listingId;

            // Check if the user is authenticated
            //if (user.is_authenticated){
                // Toggle the heart icon class
                //this.classList.toggle('fas');
                //this.classList.toggle('far');

                // Send an AJAX request to toggle watchlist status
                fetch(`/toggle_watchlist/${listingId}/`) // ---- this one is using previous 'toggle_watchlist' view ---
                //fetch("api/status")
                    .then(response => response.json())
                    .then(data => {
                        // Update the icon state

                        //this.classList.toggle('fas', data.is_watchlisted);
                        //this.classList.toggle('far', !data.is_watchlisted);
                        watchlistIcon.className = data.is_watchlisted ? 'on' : 'off';
                        watchlistIcon.innerHTML = data.is_watchlisted ? 'Watchlisted' : 'Not Watchlisted';
                    })
                    .catch(error => console.error('Error:', error));
            //}
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const commentForm = document.getElementById('comment-form');
    console.log(commentForm)
    const commentsContainer = document.getElementById('comments-container');
    console.log(commentsContainer)

    if (commentForm) {
        commentForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission

            //const comment = document.querySelector('#comment').value;
            //console.log(comment)

            // Check if the user is authenticated
            //if (user.is_authenticated){
                const formData = new FormData(commentForm);

                // Send an AJAX request to add a new comment
                fetch(commentForm.action, {
                    method: 'POST',
                    body: formData,
                })
                    .then(response => response.text())
                    .then(data => {
                        // Append the new comment to the comments container
                        //commentsContainer.innerHTML += 'You commented: '+comment+'';
                        var comment = JSON.parse(data)
                        //comment = data['text']
                        comment = comment.text
                        console.log(comment)
                        commentsContainer.innerHTML += 'You commented: '+comment+'<br>';
                        // Clear the comment form
                        commentForm.reset();//clear whats written in the text box
                    })
                    .catch(error => console.error('Error:', error));
            //}
        });
    }
});
