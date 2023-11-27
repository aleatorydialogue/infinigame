document.getElementById('user-action-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const userInputField = document.getElementById('user-input');
    const userInput = userInputField.value;

    fetch('/game/api/', { 
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('game-text').innerText = data.game_text; // Update the text with LLM output
        userInputField.value = ''; // Clear the input field after submitting
        var imageUrl = '/media/output.png?t=' + new Date().getTime(); // Update the image with a new timestamp
        document.getElementById('game-image').src = imageUrl;
    })
    .catch(error => console.error('Error:', error));
});

// Function to get CSRF token from cookies - required for POST requests in Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
