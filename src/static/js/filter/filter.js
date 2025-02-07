document.addEventListener('DOMContentLoaded', function () {
    const stationSelect = document.getElementById('stationSelect');
    const token = localStorage.getItem('access_token');

    // Fetch station data from the backend
    makeApiRequest('/api/stations', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}` // Include the JWT token in the Authorization header
        }
        })
        .then(data => {
            // Clear existing options
            stationSelect.innerHTML = '';

            // Add a default option
            const defaultOption = document.createElement('option');
            defaultOption.textContent = 'Select Any Station';
            defaultOption.disabled = true;
            stationSelect.appendChild(defaultOption);

            // Populate select options dynamically
            if (Array.isArray(data) && data.length > 0) {
                data.forEach(station => {
                    const option = document.createElement('option');
                    option.value = station.id;  // Use station ID as the value
                    option.textContent = station.station_name;  // Use station name for display text
                    stationSelect.appendChild(option);
                });
            } else {
                const noDataOption = document.createElement('option');
                noDataOption.textContent = 'No stations available';
                stationSelect.appendChild(noDataOption);
            }
        })
        .catch(error => {
            console.error('Error fetching stations:', error);
        });
});

document.addEventListener('DOMContentLoaded', function () {
    const filterDataForm = document.getElementById('filterDataForm');
    if (filterDataForm) {
        filterDataForm.addEventListener('submit', function(event) {
            event.preventDefault();  // Prevent the form from submitting normally

            const formData = new FormData(filterDataForm);
            // Get filter values from the form
            const filterData = {
                date: formData.get('date'),
                start_time: formData.get('start_time'),
                end_time: formData.get('end_time'),
                step_min: formData.get('step_min'),
                station_id: formData.get('station_id')
            };

            const token = localStorage.getItem('access_token'); // Assuming you store JWT in localStorage

            // console.log(filterData);

            // Make POST request to the Flask API
            makeApiRequest('/api/filter', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`  // Include the JWT token in the Authorization header
                },
                body: JSON.stringify(filterData)  // Send the filter data in the body of the request
            })
            .then(data => {
                // Clear old project table data
                const precipDataTable = document.getElementById('precipDataTable');
                precipDataTable.innerHTML = '';
                
                // Append new filtered data to the table
                if (Array.isArray(data) && data.length > 0) {
                    data.forEach(item => {
                        const row = `
                            <tr>
                                <td>${item.precip_time}</td>
                                <td>${item.precip_rate}</td>
                                <td>${item.precip_accum}</td>
                                <td>${item.precip_accum_long}</td>
                            </tr>
                        `;
                        precipDataTable.innerHTML += row;
                    });
                } else {
                    // Display a message if no data is returned
                    const noDataRow = `<tr><td colspan="4" class="fw-bold fs-6">No data available for the selected filters.</td></tr>`;
                    precipDataTable.innerHTML += noDataRow;
                }

            })
            .catch(error => {
                console.error('Error fetching filtered data:', error);
            });
        });
    }
});
