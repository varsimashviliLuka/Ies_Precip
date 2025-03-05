// Open the modal for editing a User record
function openUserModal() {
    const token = localStorage.getItem('access_token');
    const emailText = document.getElementById('emailSpan');
    const roleText = document.getElementById('roleSpan');
    fetch(`/api/user`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,  // Include the JWT token
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            if (response.status === 401) {
                showAlert('danger', 'სესიის ვადა ამოიწურა. გთხოვთ, თავიდან შეხვიდეთ სისტემაში.');
                clearSessionData();
            } else if (response.status === 403) {
                showAlert('danger', 'არ გაქვთ უფლებები ამ მონაცემების ნახვისთვის.');
            } else {
                showAlert('danger', 'მოხდა შეცდომა მონაცემების გამოთხოვისას.');
            }
            throw new Error('Network response was not ok.');
        }
        return response.json();
    })
    .then(data => {
        if (data) {
            document.getElementById('userUUID').value = data.uuid;
            emailText.textContent = data.email;
            roleText.textContent = data.role;

            // Show the update button only if the role is Admin
            if (data.role === 'Admin') {
                accountsButton.style.display = 'block';
            }
        } else {
            showAlert('danger', 'მომხმარებელი არ მოიძებნა.');
        }
    })
    .catch(error => console.error('Error fetching data:', error));


    const userModal = new bootstrap.Modal(document.getElementById('userModal'));
    userModal.show();
}

// Redirect to the accounts page
function redirectToAccounts() {
    window.location.href = '/accounts';
}


function changePassword(){

    const emailSpan = document.getElementById('emailSpan').innerHTML;

    const formData = {
        modalEmail: emailSpan
    };

    makeApiRequest('/api/request_reset_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)

    }).then(data => {
        if (data.message) {
            showAlert('alertPlaceholder', 'success', data.message || ' გთხოვთ შეამოწმოთ ელ.ფოსტა, ვერიფიკაციის ლინკი გამოგზავნილია.');
            
            // Close the modal 
                closeModal('userModal');
        } else {
            showAlert('alertPlaceholder', 'danger', data.error || ' გაუმართავი ელ.ფოსტა.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });


}
