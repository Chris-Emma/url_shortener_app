document.getElementById('urlForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const originalUrl = document.getElementById('originalUrl').value;
    const resultDiv = document.getElementById('result');
    const shortenedUrlDiv = document.getElementById('shortenedUrl');
    const shortUrlLabel = document.getElementById('shortUrl');
    const adminUrlLabel = document.getElementById('adminUrl');

    fetch('/shorten', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ original_url: originalUrl })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            resultDiv.textContent = `Error: ${data.error}`;
            shortenedUrlDiv.classList.add('hidden');
        } else {
            resultDiv.textContent = '';
            shortUrlLabel.innerHTML = `<a href="${data.short_url}" target="_blank">${data.short_url}</a>`;
            adminUrlLabel.innerHTML = `<a href="${data.admin_url}" target="_blank">${data.admin_url}</a>`;
            shortenedUrlDiv.classList.remove('hidden');
        }
    })
    .catch(error => {
        resultDiv.textContent = `Error: ${error}`;
        shortenedUrlDiv.classList.add('hidden');
    });
});

document.getElementById('contactForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;
    const contactResult = document.getElementById('contactResult');

    // For now, we'll just log the contact form data to the console
    console.log('Contact Form Data:', { name, email, message });

    contactResult.textContent = 'Thank you for your message. We will get back to you shortly.';
});
