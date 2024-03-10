// script.js

document.addEventListener('DOMContentLoaded', () => {
    // Event listener for the registration form submission
    const registrationForm = document.getElementById('registration-form');
    registrationForm.addEventListener('submit', (e) => {
        e.preventDefault(); // Prevent default form submission
        // Retrieves values from form inputs
        const name = e.target.elements['name'].value;
        const email = e.target.elements['email'].value;
        const password = e.target.elements['password'].value;

        // Basic client-side validation for password length
        if (password.length < 8) {
            alert('Password must be at least 8 characters long.');
            return; // Stops the function if validation fails
        }

        // Handle registration (send data to server, etc.)
        fetch('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, email, password }),
        })
            .then(handleFetchResponse)
            .then(data => {
                displaySuccessMessage('Registration successful', 'registration-form');
                window.location.href = '/'; // Replace '/welcome with correct path
            })
            .catch(error => {
                // Log the error and display a message to the user
                console.error('There has been a problem with your fetch operation:', error);
                displayErrorMessage(error.message, 'registration-form');
            });
    });

    // Login Form Event Listener
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission
        // Extract input values
        const email = loginForm.elements['email'].value;
        const password = loginForm.elements['password'].value;

        // Handle login (send data to server, etc.)
        // You can make an AJAX request here to send form data to the server for login
        fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        })
            .then(handleFetchResponse)
            .then(data => {
                displaySuccessMessage('Login successful', 'login-form');
                window.location.href = '/dashboard'; // Replace '/dashboard with correct path
            })
            .catch(error => {
                // Log the error and display a message to the user
                console.error('There has been a problem with your fetch operation:', error);
                displayErrorMessage(error.message, 'login-form');
            });
    });

    // Video Submission Form Event Listener
    const videoSubmissionForm = document.getElementById('video-submission-form');
    videoSubmissionForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission
        // Extract input values
        const videoUrl = videoSubmissionForm.elements['video-url'].value;

        // Handle video submission (send data to server, etc.)
        // You can make an AJAX request here to send video URL to the server for processing
        // Replace '/login' with your video submission endpoint
        fetch('/api/url/' + videoUrl)
            .then(handleFetchResponse)
            .then(data => {
                displaySuccessMessage('Video submission successful', 'video-submission-form');
            })
            .catch(error => {
                // Log the error and display a message to the user
                console.error('There has been a problem with your fetch operation:', error);
                displayErrorMessage(error.message, 'video-submission-form');
            });
    });
});

// Function to display error message
function displayErrorMessage(message, formId) {
    // Clear existing messages
    clearMessages(formId);
    const errorElement = document.createElement('p');
    errorElement.setAttribute('role', 'alert');
    errorElement.classList.add('error-message');
    errorElement.textContent = message;
    // Append error message to a suitable location on the page (e.g., inside the form)
    document.getElementById(formId).appendChild(errorElement);
}

// Function to display success message
function displaySuccessMessage(message, formId) {
    // Clear existing messages
    clearMessages(formId)
    const successElement = document.createElement('p');
    successElement.setAttribute('role', 'alert');
    successElement.classList.add('success-message');
    successElement.textContent = message;
    // Append success message to a suitable location on the page (e.g., inside the form)
    document.getElementById(formId).appendChild(successElement);
}

function clearMessages(formId) {
    const form = document.getElementById(formId);
    const existingMessages = form.querySelectorAll('.error-message, .success-message');
    existingMessages.forEach(msg => msg.remove());
}

function handleFetchResponse(response) {
    const statusImage = document.getElementById('status-image');
    statusImage.src = "http://http.cat/" + response.status + ".jpg";

    if (!response.ok) {
        // Handle common HTTP errors
        if (response.status === 404) {
            throw new Error('Not found');
        } else if (response.status === 401) {
            throw new Error('Not authorized');
        } else {
            // Generic error for other statuses
            throw new Error('An error occured: ' + response.statusText);
        }
    }
    // Check if the response is JSON before parsing
    if (response.headers.get('Content-Type')?.includes('application/json')) {
        return response.json();
    }
    throw new Error('Invalid JSON response from server');
}
