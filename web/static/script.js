// script.js

document.addEventListener('DOMContentLoaded', () => {
    // Hide the loading spinner initially
    document.getElementById('loading-spinner').style.display = 'none';

    // Fetch and display transcriptions upon page load
    fetchAndDisplayTranscriptions();

    // Event listener for the transcription form submission
    const transcriptionForm = document.getElementById('transcription-form');
    transcriptionForm.addEventListener('submit', (e) => {
        e.preventDefault(); // Prevent default form submission

        // Extract the YouTube URL from the form
        const youtubeUrl = transcriptionForm.elements['youtube-url'].value;

        // Show the loading spinner
        document.getElementById('loading-spinner').style.display = 'block';

        // Attempt to extract the video ID and submit it for transcription
        const videoId = extractVideoId(youtubeUrl);
        if (!videoId) {
            displayErrorMessage('Invalid YouTube URL.', 'transcription-form');
            document.getElementById('loading-spinner').style.display = 'none';
            return;
        }

        // Handle the transcription request
        handleTranscriptionRequest(videoId);
    });
    
    /*
    // Registration Form Event Listener
    const registrationForm = document.getElementById('registration-form');
    registrationForm.addEventListener('submit', (e) => {
        // Registration form submission logic
    });

    // Login Form Event Listener
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', (event) => {
        // Login form submission logic
    });
    */
});

// Function to fetch and display transcriptions
function fetchAndDisplayTranscriptions() {
    fetch('/api/transcriptions')
        .then(response => response.json())
        .then(transcriptions => {
            const list = document.getElementById('transcriptions-list');
            list.innerHTML = ''; // Clear the list
            transcriptions.forEach(transcription => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `<a href="#" onclick="fetchTranscriptionDetails('${transcription.id}')">${transcription.url}</a>`;
                list.appendChild(listItem);
            });
        })
        .catch(error => console.error('Failed to fetch transcriptions:', error));
}

// Function to fetch transcription details
function fetchTranscriptionDetails(transcriptionId) {
    // Fetch and display details for a specific transcription
}

// Function to handle transcription request submission
function handleTranscriptionRequest(videoId) {
    fetch(`/api/transcribe/${videoId}`, {
        method: 'POST', // or 'GET' if that's what your API requires
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(handleFetchResponse)
    .then(data => {
        displaySuccessMessage('Transcription in progress. You will be notified upon completion.', 'transcription-form');
        document.getElementById('loading-spinner').style.display = 'none';
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
        displayErrorMessage(error.message, 'transcription-form');
        document.getElementById('loading-spinner').style.display = 'none';
    });
}

// Function to extract video ID from Youtube URL
function extractVideoId(url) {
    const videoIdMatch = url.match(/[?&]v=([^?&]+)/);
    return videoIdMatch ? videoIdMatch[1] : null;
}

// Display error message
function displayErrorMessage(message, formId) {
    clearMessages(formId);
    // Error message logic
}

// Display success message
function displaySuccessMessage(message, formId) {
    clearMessages(formId);
    // Success message logic
}

// Clear messages
function clearMessages(formId) {
    // Logic to clear messages
}

// Handle fetch response
function handleFetchResponse(response) {
    // Logic to handle the fetch response
}
