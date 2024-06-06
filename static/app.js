document.addEventListener('DOMContentLoaded', () => {
    const services = ["OneCloud", "XCloud", "Backend", "HMSWeb", "Analytics", "Streaming", "API Gateway", "Partner", "Messaging"];
    const centerDashboard = document.getElementById('center-dashboard');

    // Create buttons dynamically
    services.forEach(service => {
        const button = document.createElement('button');
        button.className = 'dashboard-item';
        button.innerText = service;
        centerDashboard.appendChild(button);

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
    const alertsButton = document.getElementById('alerts-button');
    if (alertsButton) {
        alertsButton.addEventListener('click', () => {
            window.location.href = '/alerts-page';
        });
    }

    const fetchIncidentData = async () => {
        try {
            const response = await fetch('/api/events', {
                headers: {
                    'Authorization': 'apitoken pncHtgATRjep2fo0poggJQ'
                }
            });

            if (!response.ok) {
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

        openIncidents.forEach(event => {
            const row = document.createElement('tr');

            const titleCell = document.createElement('td');
            titleCell.textContent = event.problem || 'N/A';
            row.appendChild(titleCell);

            const onCell = document.createElement('td');
            onCell.textContent = event.entityLabel || 'N/A';
            row.appendChild(onCell);

            const startedCell = document.createElement('td');
            startedCell.textContent = event.start ? new Date(event.start).toLocaleString() : 'N/A';
            row.appendChild(startedCell);

            const endCell = document.createElement('td');
            endCell.textContent = event.end ? new Date(event.end).toLocaleString() : 'N/A';
            row.appendChild(endCell);

            const timelineCell = document.createElement('td');
            timelineCell.textContent = event.state || 'N/A';
            row.appendChild(timelineCell);

            tableBody.appendChild(row);
        });
    };

    const updateServiceAlerts = (data) => {
        const openIncidents = data.filter(event => event.type === 'incident' && event.state === 'open');
        const serviceButtons = document.querySelectorAll('.dashboard-item');

        serviceButtons.forEach(button => {
            const serviceName = button.innerText.toLowerCase();
            const hasAlert = openIncidents.some(incident => incident.entityLabel.toLowerCase().includes(serviceName));

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

        // Additional code to handle tab content display if necessary
    };

    fetchIncidentData();
});
