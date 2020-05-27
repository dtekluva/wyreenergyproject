var host = window.location.hostname == 'localhost'
    ? 'http://localhost:8000/'
    : 'http://' + window.location.hostname + '/';

if (location.protocol == 'https:') {
  // page is secure
  host = host.replace("http", "https")
};

const cdd_upload_url = 'upload_cdd/';


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
    html: '<strong>UPLOADING CDD DATA..</strong>.', 
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
    url: host + cdd_upload_url,
    data: formData,
    contentType: false,
    cache: false,
    processData: false,
    success: function (response, textStatus, jqXHR) {
      response = JSON.parse(response);

      if (response.response == "success"){
        document.getElementById("dropzone").style.backgroundColor = `#baddbb`
        Swal.close()
        Swal.close()
        swal({
          title: "Success",
          text: "Successfully Uploaded CDDs.!!",
        });
      } else{
        Swal.close()
        swal({
          title: "Success",
          text: "Failed To Upload CDDs.!!",
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

