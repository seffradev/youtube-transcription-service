// script.js

document.addEventListener('DOMContentLoaded', () => {
    // Fetch and display transcriptions upon page load
    fetchAndDisplayTranscriptions();

    // Event listener for the transcription form submission
    const transcriptionForm = document.getElementById('transcription-form');
    transcriptionForm.addEventListener('submit', (e) => {
        e.preventDefault(); // Prevent default form submission

        // Extract the YouTube URL from the form
        const youtubeUrl = transcriptionForm.elements['youtube-url'].value;

        // Attempt to extract the video ID and submit it for transcription
        const videoId = extractVideoId(youtubeUrl);
        if (!videoId) {
            displayErrorMessage('Invalid YouTube URL.', 'transcription-form');
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
        .then(response => {
            const list = document.getElementById('transcriptions-list');
            list.innerHTML = ''; // Clear the list
            transcriptions = response.transcriptions || [];
            transcriptions.forEach(transcription => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `<a href="/transcriptions/${transcription.id}">${transcription.id} - ${transcription.requested_at} - ${transcription.completed_at}</a>`;
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
    fetch(`/api/transcribe/${videoId}`)
    .then(handleFetchResponse)
    .then(data => {
        displaySuccessMessage('Transcription in progress. You will be notified upon completion.', 'transcription-form');
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
        displayErrorMessage(error.message, 'transcription-form');
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
