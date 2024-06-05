document.addEventListener('DOMContentLoaded', () => {
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
        } catch (error) {
            console.error('Error fetching incident data:', error);
        }
    };

    const displayIncidentData = (data) => {
        const tableBody = document.getElementById('incident-data');
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
