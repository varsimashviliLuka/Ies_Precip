// Open the modal for creating or editing a GeophysicSeismic record
function openExportCSVModal() {
    const modal = new bootstrap.Modal(document.getElementById('ExportCSV'));
    modal.show();

}


// Get the button element
const exportButton = document.getElementById('exportButton');
const loadingMessage = document.getElementById('loadingMessage');

// Add event listener to the button
exportButton.addEventListener('click', function () {
    // Show loading message
    loadingMessage.style.display = 'block';
    exportButton.disabled = true; // Disable the button to prevent multiple clicks

    // Prepare the request body with the parameters
    const exportData = {
        date: '2025-02-10',
        start_time: '00:00:00',
        end_time: '23:59:59',
        step_min: 5,
        station_id: 1, // Example station_id
        format: 'csv' // You can choose the desired format
    };

    // Send POST request to the Flask API
    fetch('/api/export', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Add the JWT token if needed
        },
        body: JSON.stringify(exportData)
    })
    .then(response => {
        if (response.ok) {
            // If the response is OK, process the CSV file download
            return response.blob(); // We expect the server to send the file as a blob
        } else {
            throw new Error('Failed to export data');
        }
    })
    .then(blob => {
        // Create a URL for the blob and trigger a download
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'export.csv'; // Specify the filename
        a.style.display = 'none';
        document.body.appendChild(a);
        
        // Trigger the download
        a.click();
        
        // Clean up by revoking the object URL and removing the download link
        URL.revokeObjectURL(url);
        document.body.removeChild(a);
    })
    .catch(error => {
        console.error('Error exporting data:', error);
    })
    .finally(() => {
        // Hide loading message and re-enable the button
        loadingMessage.style.display = 'none';
        exportButton.disabled = false;
    });
});
