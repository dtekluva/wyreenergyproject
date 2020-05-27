var host = window.location.hostname == 'localhost'
    ? 'http://localhost:8000/'
    : 'http://' + window.location.hostname + '/';

if (location.protocol === 'https:') {
      // page is secure
      host = host.replace("http", "https")
};

const image_upload_url = 'upload_image/';
const details_update_url = 'update_details/'; 
const password_update_url = 'auth/update_password/'; 

var old_password = document.getElementById("old_password")
var new_password = document.getElementById("new_password")
var retype_password = document.getElementById("retype_password")
var password_button = document.getElementById("password_button")

$(window).on('load', ()=> {
  $("#dropzone").click(function () {
    $("#image").click();
  });

  $("#password_button").click((e)=>{
      let data = verify_pass();
      if (data[0]){
        update_password(data[1], data[2])
      };

  });
  
})

                         ///////////////////////UPDATE IMAGE//////////////////////

var formData;
$('#image').change( (e)=>{

  e.preventDefault()
  formData = new FormData();
  formData.append('file', e.target.files[0]);
  Swal.fire({
    title: 'PROCCESSING PLEASE WAIT !!!',
    html: '<strong>UPDATING IMAGE..</strong>.', 
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
    url: host + image_upload_url,
    data: formData,
    contentType: false,
    cache: false,
    processData: false,
    success: function (response, textStatus, jqXHR) {
      response = JSON.parse(response);
      document.getElementById("dropzone").style.backgroundImage = `url('${host.slice(0, -1) + response.message}')`
      Swal.close()
      Swal.close()
      swal({
        title: "Success",
        text: "Successfully Uploaded Image.!!",
      });
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


$('#new-branch-button').click( (e)=>{

  e.preventDefault()
  formData = new FormData();
  let name = document.getElementById("fname");
  let username = document.getElementById("username");
  let phone = document.getElementById("phone");
  let address = document.getElementById("address");

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
    url: host + details_update_url,
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
          text: "Successfully Updated Profile.!!",
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

var update_password = ((new_password, old_password)=>{

      formData = new FormData();

      formData.append('old', old_password);
      formData.append('new', new_password);

      Swal.fire({
        title: 'PROCCESSING PLEASE WAIT !!!',
        html: '<strong>UPDATING PASSWORD..</strong>.', 
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
        url: host + password_update_url,
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (response, textStatus, jqXHR) {
          response = JSON.parse(response);

          if (response.response == "success"){
              Swal.close()
              swal({
                title: "Success",
                text: "Successfully Changed Password.!!",
              });
              window.location.reload();
            }else{
              Swal.close()
              swal({
                title: "Update Failed",
                text: "Incorrect Old Password.!!",
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

var verify_pass = (()=>{

  if (new_password.value.length >= 8){

    if (new_password.value == retype_password.value){

        if (old_password.value.length >= 8){

          return [true, new_password.value, old_password.value]

        }else{
          swal({
            title: "No Value For Old Password",
            text: "Please enter your old password.!!",
          });
          return [false];
        }
    }
    else{
      swal({
        title: "Password Mismatch",
        text: "Sorry new password and retype Passwords do not match.!!",
      });
    }
      return [false]
    }else{
      swal({
        title: "Bad Password",
        text: "Please enter at least 8 characters.!!",
      });
      return [false]
    }
})
