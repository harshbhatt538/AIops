document.addEventListener('DOMContentLoaded', () => {
    // Redirect to login if not authenticated
    fetch('/protected', {
        method: 'GET',
        credentials: 'include'  // Include cookies with the request
    }).then(response => {
        if (!response.ok) {
            window.location.href = '/login';
        }
    });

    const services = ["OneCloud", "XCloud", "Backend", "HMSWeb", "Analytics", "Streaming", "API Gateway", "Partner", "Messaging"];
    const centerDashboard = document.getElementById('center-dashboard');

    // Create buttons dynamically
    services.forEach(service => {
        const button = document.createElement('button');
        button.className = 'dashboard-item';
        button.innerText = service;
        centerDashboard.appendChild(button);

        button.addEventListener('click', () => {
            const serviceName = button.innerText;

            fetch('/chart-page', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',  // Include cookies with the request

                body: JSON.stringify({ service_name: serviceName })
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => { throw new Error(data.message) });
                }
                return response.text();
            })
            .then(html => {
                document.open();
                document.write(html);
                document.close();
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    // Event listener for the "Alerts" button
    const alertsButton = document.getElementById('alerts-button');
    if (alertsButton) {
        alertsButton.addEventListener('click', () => {
            window.location.href = '/alerts-page';
        });
    }

    const modifyServiceButton = document.getElementById('modifyService-button');
    if (modifyServiceButton) {
        modifyServiceButton.addEventListener('click', () => {
            window.location.href = 'http://127.0.0.1:5000/modify-service';
        });
    }

    $(document).ready(function() {
        // Login form submission
        $('#login-form').on('submit', function(e) {
            e.preventDefault();
            var formData = {
                'username': $('#username').val(),
                'password': $('#password').val()
            };

            $.ajax({
                type: 'POST',
                url: '/login',
                contentType: 'application/json',
                data: JSON.stringify(formData),
                success: function(response) {
                    window.location.href = '/';
                },
                error: function(response) {
                    alert(response.responseJSON.error);
                }
            });
        });
    });

    const fetchIncidentData = async () => {
        try {
            const response = await fetch('/api/events', {
                credentials: 'include'  // Include cookies with the request
            });

            if (!response.ok) {
                if (response.status === 401) {
                    console.error('Unauthorized access, redirecting to login.');
                    window.location.href = '/login';
                }
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            console.log('API Response:', data);  // Log the API response to the console
            displayIncidentData(data);
            updateServiceAlerts(data);
        } catch (error) {
            console.error('Error fetching incident data:', error);
        }
    };

    const displayIncidentData = (data) => {
        const tableBody = document.getElementById('incident-data');
        if (!tableBody) {
            console.error('Element with ID "incident-data" not found.');
            return;
        }

        tableBody.innerHTML = ''; // Clear previous data

        // Filter the events to include only those with type "incident" and state "open"
        const openIncidents = data.filter(event => event.type === 'incident' && event.state === 'open');

        openIncidents.forEach(incident => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${incident.id}</td>
                <td>${incident.entityLabel}</td>
                <td>${incident.type}</td>
                <td>${incident.state}</td>
                <td>${incident.start}</td>
                <td>${incident.end}</td>
            `;
            tableBody.appendChild(row);
        });
    };


    const updateServiceAlerts = (data) => {
        const openIncidents = data.filter(event => event.type === 'incident' && event.state === 'open');
        const serviceButtons = document.querySelectorAll('.dashboard-item');

        serviceButtons.forEach(button => {
            const serviceName = button.innerText.toLowerCase();
            const hasAlert = openIncidents.some(incident => incident.problem.toLowerCase().includes(serviceName));

            if (hasAlert) {
                button.style.backgroundColor = 'red';
            } else {
                button.style.backgroundColor = '';
            }
        });
    };


    const showTab = (tabName) => {
        const tabs = document.querySelectorAll('.tab-button');
        tabs.forEach(tab => {
            tab.classList.remove('active');
            if (tab.textContent.toLowerCase() === tabName.toLowerCase()) {
                tab.classList.add('active');
            }
        });
    };

    fetchIncidentData();
});
