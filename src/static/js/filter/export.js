// გახსენი მენიუ CSV ექსპორტისთვის
function openExportCSVModal() {
    fetchExportCSVData(); // მიიღე სადგურების მონაცემები
    const modal = new bootstrap.Modal(document.getElementById('ExportCSV'));
    modal.show(); // აჩვენე მენიუ
}

const token = localStorage.getItem('access_token'); // JWT ტოკენის აღება ადგილობრივ შენახვიდან

// სადგურების მონაცემების გამოტანა
function fetchExportCSVData() {
    const stationList = document.getElementById("stationList");

    // სადგურების მონაცემების მიღება API-სგან
    makeApiRequest('/api/stations', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}` // JWT ტოკენის დამატება ავტორიზაციისთვის
        }
    })
    .then(data => {
        // გასუფთავება არსებული ჩექბოქსებისგან
        stationList.innerHTML = '';
        const checkbox = document.createElement("li");
        checkbox.innerHTML = `
            <label class="dropdown-item">
                <input type="checkbox" id="selectAll"> ყველა სადგურის არჩევა
            </label>
            <hr>
        `;
        stationList.appendChild(checkbox);
        data.forEach(station => {
            const li = document.createElement("li");
            li.innerHTML = `
                <label class="dropdown-item text-start">
                    <input type="checkbox" class="station-checkbox" value="${station.id}"> ${station.station_name}
                </label>
            `;
            stationList.appendChild(li);
        });

        addEventListeners(); // დაამატე სადგურების ჩართვის/გამორთვის მოვლინები
    })
    .catch(error => {
        console.error('Error fetching stations:', error); // შეცდომა სადგურების მიღებისას
    });
}

// მოვლენის მსვლელობები ჩაამატე ჩექბოქსებზე
function addEventListeners() {
    const selectAll = document.getElementById("selectAll");
    const checkboxes = document.querySelectorAll(".station-checkbox");

    // ყველა სადგურის არჩევა/გაუქმება
    selectAll.addEventListener("change", function() {
        checkboxes.forEach(cb => cb.checked = selectAll.checked); // ყველა სადგურის ჩართულობა
        updateSelection(); // განაახლე რაოდენობა
    });

    checkboxes.forEach(cb => {
        cb.addEventListener("change", function() {
            if (!this.checked) {
                selectAll.checked = false; // თუ ერთ-ერთი ჩექბოქსი გამორთულია, ყველა სადგური გამორთულია
            } else if ([...checkboxes].every(cb => cb.checked)) {
                selectAll.checked = true; // თუ ყველა ჩექბოქსი მონიშნულია, "select all" ჩაერთოს
            }
            updateSelection(); // განაახლე რაოდენობა
        });
    });
}

// განაახლე არჩეული სადგურების რაოდენობა
function updateSelection() {
    const selectedStations = document.getElementById("selectedStations");

    const checkedStations = document.querySelectorAll(".station-checkbox:checked");
    selectedStations.textContent = checkedStations.length; // აჩვენე არჩეული სადგურების რაოდენობა
}

// ფორმის გამოგზავნა
document.getElementById('ExportCSVForm').onsubmit = submitExportCSVForm;

function submitExportCSVForm(event) {
    event.preventDefault(); // ფორმის ჩვეულებრივი გამოგზავნა გადაგვაქვს
    // შექმენი მონაცემები, რომლებიც გადაეცემა API-ს
    const formData = new FormData(document.getElementById('ExportCSVForm'));
    const exportData = {
        start_date: formData.get('start_date'),
        start_time: formData.get('start_time'),
        end_date: formData.get('end_date'),
        end_time: formData.get('end_time'),
        step_min: formData.get('step_min'),
        station_ids: [] // დაამატე არჩეული სადგურების ID-ები
    };

    const selectedStations = document.querySelectorAll(".station-checkbox:checked");
    if (selectedStations.length <= 0) {
        showAlert('alertDiv', 'danger', 'გთხოვთ მონიშნოთ რომელიმე სადგური.'); // შეტყობინების ჩვენება თუ სადგური არ არის არჩეული
    } else {
        selectedStations.forEach(station => {
            exportData.station_ids.push(station.value); // დაამატე არჩეული სადგურის ID
        });
        makeExportCSV(exportData); // დაიწყე CSV ექსპორტი
    }
};

const exportButton = document.getElementById('submitExportCSVlBtn');
const loadingMessage = document.getElementById('loadingMessage');

// CSV ფაილის ექსპორტი
function makeExportCSV(exportCSV){
    loadingMessage.style.display = 'block'; // აჩვენე დატვირთვის შეტყობინება
    exportButton.disabled = true; // გამორთე ღილაკი
    const startDate = document.getElementById('exportStartDate').value;
    const endDate = document.getElementById('exportEndDate').value;
    // გამოგზავნე POST მოთხოვნა Flask API-სთან
    fetch('/api/export', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // JWT ტოკენის დამატება
        },
        body: JSON.stringify(exportCSV) // მონაცემების გადაცემა JSON ფორმატში
    })
    .then(response => {
        if (response.status === 401) {
            showAlert('alertDiv', 'danger', 'გთხოვთ ხელახლა გაიაროთ ავტორიზაცია.'); // ავტორიზაციის შეცდომა
            clearSessionData(); // სესიის მონაცემების გაწმენდა
            return Promise.reject('Unauthorized');
        }
        if (!response.ok) {
            throw new Error('Failed to export data'); // შეცდომა ექსპორტირების დროს
        }
        return response.blob(); // დაბრუნდება CSV ფაილი
    })
    .then(blob => {
        const url = URL.createObjectURL(blob); // შექმენი URL ბლობისთვის
        const a = document.createElement('a');
        a.href = url;
        
        a.download = `${startDate}_${endDate}.csv`; // განუსაზღვრე ფაილის სახელწოდება
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click(); // ჩამოიწერე CSV ფაილი

        URL.revokeObjectURL(url); // წაშალე URL
        document.body.removeChild(a); // წაშალე ელემენტი
    })
    .catch(error => {  
        showAlert('alertDiv', 'danger', 'Error: გაუმართავი CSV ფაილის გადმოწერა.'); // შეცდომა
        console.error('Error exporting data:', error); // შეცდომის ლოგირება
    })
    .finally(() => {
        loadingMessage.style.display = 'none'; // დამალე დატვირთვის შეტყობინება
        exportButton.disabled = false; // კვლავ გაააქტიურე ღილაკი
    });
}
