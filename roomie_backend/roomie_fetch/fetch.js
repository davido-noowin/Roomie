// Fetch the accomodation data from user
function grabAccommodationData(data)
{
    fetch("roomAccommodations", "GET")
    .then( res => console.log(res))
    .catch( err => console.log(err))
    data.preventDefault()
}