$.ajax({
    url: 'http://3.133.161.88:8000/roomInfo/',  // URL of the Django view
    type: 'GET',
    dataType: 'json',
    success: function(response) {
      // Handle the response from the server
      console.log(response);

      const keys = Object.keys(response)
      console.log(keys)
      // Do something with the room information

    },
    error: function(xhr, status, error) {
      // Handle error
      console.log(error);
    }
  });


  $.ajax({
    url: 'http://3.133.161.88:8000/roomAccomodations/',  // URL of the Django view
    type: 'GET',
    dataType: 'json',
    success: function(response) {
      // Handle the response from the server
      console.log(response);

      const accomodations = Object.keys(response)
      console.log(accomodations)
      // Do something with the room information

    },
    error: function(xhr, status, error) {
      // Handle error
      console.log(error);
    }
  });