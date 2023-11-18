var btn = document.getElementById('watchlist_button');

function watchlist_button_click()
{
    fetch('../watchlist_add_or_remove/' + '{{ listing.id }}');
    
    // Add listing to watchlist
    if (btn.dataset.value === "False")
    {
        btn.dataset.value = true;
        btn.src = "{% static 'icons/heart-fill.png' %}";
        btn.className = watchlist_button_remove;
    }
    // Remove listing from watchlist
    else
    {
        btn.value = false;
        btn.src = "{% static 'icons/heart-line.png' %}"
        btn.className = watchlist_button_add;
    }
}