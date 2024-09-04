document.addEventListener('DOMContentLoaded', function() {
    // Example: Add event listeners to forms
    const clientForm = document.getElementById('client-form');
    if (clientForm) {
        clientForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission
            validateClientForm();
        });
    }
    
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission
            validateContactForm();
        });
    }
});

function validateClientForm() {
    const name = document.getElementById('name').value.trim();
    if (!name) {
        alert('Client name is required.');
        return;
    }
    
    // If validation passes, submit the form
    document.getElementById('client-form').submit();
}

function validateContactForm() {
    const name = document.getElementById('name').value.trim();
    const surname = document.getElementById('surname').value.trim();
    const email = document.getElementById('email').value.trim();
    
    if (!name || !surname || !email) {
        alert('All fields are required.');
        return;
    }
    
    if (!validateEmail(email)) {
        alert('Invalid email address.');
        return;
    }
    
    // If validation passes, submit the form
    document.getElementById('contact-form').submit();
}

function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

document.addEventListener('DOMContentLoaded', function() {
    const clientForm = document.getElementById('client-form');
    if (clientForm) {
        clientForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission
            const formData = new FormData(clientForm);

            fetch('/clients/new', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/clients';
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
    
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission
            const formData = new FormData(contactForm);

            fetch('/contacts/new', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/contacts';
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});
