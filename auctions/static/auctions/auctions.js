document.addEventListener('DOMContentLoaded', function() {
    console.log('Auctions.js loaded successfully!'); // to debug
    const watchlistIcon = document.getElementById('watchlist-icon');
    console.log(watchlistIcon)

    if (watchlistIcon) {
        watchlistIcon.addEventListener('click', function() {
            //const listingId = this.dataset.listingId;

            if (header.innerHTML === "<i class='far fa-heart'></i>Add to Watchlist") {
                header.innerHTML = "<i class='fas fa-heart'></i>Added to Watchlist"
            }
            else {
                header.innerHTML = "<i class='far fa-heart'></i>Add to Watchlist"
            }
            // Check if the user is authenticated
            //if (user.is_authenticated){
                // Toggle the heart icon class
                //this.classList.toggle('fas');
                //this.classList.toggle('far');

                // Send an AJAX request to toggle watchlist status
                //fetch(`/toggle_watchlist/${listingId}/`) // ---- this one is using previous 'toggle_watchlist' view ---
                //fetch("api/status")
                    //.then(response => response.json())
                    //.then(data => {
                        // Update the icon state

                        //this.classList.toggle('fas', data.is_watchlisted);
                        //this.classList.toggle('far', !data.is_watchlisted);
                        //watchlistIcon.className = data.is_watchlisted ? 'on' : 'off';
                        //watchlistIcon.innerHTML = data.is_watchlisted ? 'Watchlisted' : 'Not Watchlisted';
                    //})
                    //.catch(error => console.error('Error:', error));
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

            const formData = new FormData(commentForm);

            // Send an AJAX request to add a new comment
            fetch(commentForm.action, {
                method: 'POST',
                body: formData,
            })
                .then(response => response.text())
                .then(data => {
                    // Append the new comment to the comments container
                    var comment = JSON.parse(data)
                    comment = comment.text
                    console.log(comment)
                    commentsContainer.innerHTML += 'You commented: '+comment+'<br>';
                    // Clear the comment form
                    commentForm.reset();//clear whats written in the text box
                })
                .catch(error => console.error('Error:', error));
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const header = document.getElementById('watchlist-image')
    //console.log(header)
    const add = document.getElementById('wishlist')
    //console.log(add)
    //const listingId = this.dataset.listingId
    //console.log(listingId)

    header.addEventListener('click', function(event) {
        event.preventDefault(); // some reason this stops from executing on refresh aswell
        const listingId = this.dataset//get the listing id
        console.log(listingId)
        const number = 23;//testing on minecraft listing temp
        console.log(number)
        console.log(header.innerHTML)
        if (document.querySelector('#foo').src === "https://cdn-icons-png.flaticon.com/512/73/73814.png") {
            document.querySelector('#foo').src = "https://cdn.icon-icons.com/icons2/1369/PNG/512/-favorite_90527.png"
            //call add to watchlist function
            fetch('addwishlist/'+number+'/')//page not found
        }
        else {
            document.querySelector('#foo').src = "https://cdn-icons-png.flaticon.com/512/73/73814.png"
            //call remove from watchlist function
        }
    });
});
