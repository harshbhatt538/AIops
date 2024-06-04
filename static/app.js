document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.dashboard-item, .subpanel-item, .top-bar-btn');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const service = button.innerText;

            fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ key: 'service', value: service })
            })
            .then(response => response.json())
            .then(data => {
                if (data.errors) {
                    console.error('Error:', data.errors);
                } else {
                    console.log(data);
                    sessionStorage.setItem('apiResponse', JSON.stringify(data.items));
                    window.location.href = '/data-page';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});
