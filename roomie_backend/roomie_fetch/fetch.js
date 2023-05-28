// Fetch the accomodation data from user
fetch('roomAccommodations', { 
    method: "POST",
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name : "User 1"
    })
})
    .then(response => response.json())
    .then(data => {
        // Process the data here
        console.log(data); // Output the fetched data to the console
    })
    .catch(error => {
        console.error('Error:', error);
    });