// Fetch the accomodation data from user
function grabAccommodationData(url)
{
    fetch(url, "GET")
    .then( res => console.log(res))
    .catch( error => console.log("ERROR"))
    url.preventDefault()
}