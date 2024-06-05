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

    // Event listener for the "Alerts" button
    const alertsButton = document.querySelector('.top-bar-btn:nth-of-type(1)'); // Adjust the selector as needed
    if (alertsButton) {
        alertsButton.addEventListener('click', () => {
            window.location.href = '/alerts-page';
        });
    }
});
setInterval(function() {
[] = {BACKEND,CLOUD}
element = document.getElementsByClassName("dashboard-item")[0];
createAlert(element);

}, 10000);

const createAlert = (element) =>{
    element.style.background = 'red';
}