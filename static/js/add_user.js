var host = window.location.hostname == 'localhost'
    ? 'http://localhost:8000/'
    : 'http://' + window.location.hostname + '/';

if (location.protocol == 'https:') {
  // page is secure
  host = host.replace("http", "https")
};

const add_user = 'add_user/'; 
                         ///////////////////////UPDATE IMAGE//////////////////////

$('#dropzone').click( (e)=>{
      Swal.close()
      swal({
        title: "User Does Not Exist Yet",
        text: "Image can be added in the edit customer view..!!",
      });
  });


$('#new-branch-button').click( (e)=>{

  e.preventDefault()
  formData = new FormData();
  let name = document.getElementById("fname");
  let username = document.getElementById("username");
  let phone = document.getElementById("phone");
  let address = document.getElementById("address");

  if (!name.value || !username.value || !phone.value || !address.value){
    swal({
          title: "Field cannot be empty",
          text: "One or more fields are still empty please complete them!!",
        });
    return
  }

  var format = /[ !@#$%^&*()_+\-=\[\]{};':"\\|,.<>\~¬¦/£?]/;
  
  if (format.test(username.value)){
    swal({
          title: "Update Failed",
          text: "Invalid characters in username.!!",
        });
    return
  }

  formData.append('name', name.value);
  formData.append('phone', phone.value);
  formData.append('address', address.value);
  formData.append('username', username.value);

  Swal.fire({
    title: 'PROCCESSING PLEASE WAIT !!!',
    html: '<strong>UPDATING DETAILS..</strong>.', 
    allowOutsideClick: false
  });
  Swal.showLoading();

  // append any extra form data here

  let csrftoken = $('[name="csrfmiddlewaretoken"]')[0].value

  function csrfSafeMethod (method) {
      // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader('X-CSRFToken', csrftoken)
    }
    }
  })

  $.ajax({
    type: 'POST',
    url: host + add_user,
    data: formData,
    contentType: false,
    cache: false,
    processData: false,
    success: function (response, textStatus, jqXHR) {
      response = JSON.parse(response);
      console.log(response);
      Swal.close()
      
      if (response.response == "success"){
        Swal.close()
        swal({
          title: "Success",
          text: "Successfully Created Customer Profile.!!",
        });
      }else if (response.response == "failure"){
        Swal.close()
        swal({
          title: "Update Failed",
          text: "Invalid characters in username.!!",
        });
    }else if (response.response == "error"){
      Swal.close()
      swal({
        title: "Something Went Wrong",
        text: "Bad request Something went wrong..!!",
      });
  }else if (response.response == "user exists"){
    Swal.close()
    swal({
      title: "Something Went Wrong",
      text: "Sorry Username is already Taken..!!",
    });
}
    },
    error: function(response, textStatus, jqXHR){
      Swal.close()
      
      swal({
        title: "Something went wrong",
        text: "Please check your internet connection.!!",
      });
    }
  });
} );
