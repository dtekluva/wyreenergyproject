var host = window.location.hostname == 'localhost'
    ? 'http://localhost:8000/'
    : 'http://' + window.location.hostname + '/';

if (location.protocol == 'https:') {
  // page is secure
  host = host.replace("http", "https")
};

const image_upload_url = 'upload_image/';
const details_update_url = 'edit_user/'; 
const password_update_url = 'auth/update_password/'; 
const update_branch_url = 'update_branch/'; 
const update_device_url = 'update_device/'; 
const create_branch_url = 'create_branch/'; 
const create_device_url = 'create_device/'; 

var old_password = document.getElementById("old_password");
var new_password = document.getElementById("new_password");
var retype_password = document.getElementById("retype_password");
var password_button = document.getElementById("password_button");
var customer_id = document.getElementById("customer_id").value;

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
  formData.append('customer_id', customer_id);

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
  formData.append('customer_id', customer_id);

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
      formData.append('customer_id', customer_id);

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

//////////////////////////////////////////////////////////
///////////////////// UPDATE BRANCHES/////////////////////
//////////////////////////////////////////////////////////

let branch_forms = document.getElementsByClassName("branch")

Array.from(branch_forms).forEach((e)=>{

  e.addEventListener("submit", (e)=>{
    e.preventDefault()

    let form_data = e.target.elements;

    let branch_name = form_data[0].value;
    let address = form_data[1].value;
    let gen1 = form_data[2].value;
    let gen2 = form_data[3].value;
    
    let branch_id = e.target.getAttribute('data-branch');

    console.log(branch_name, address, gen1, gen2, branch_id);
    update_branch(branch_name, address, gen1, gen2, branch_id);
    
  })
})

var update_branch = ((branch_name, address, gen1, gen2, branch_id)=>{

  formData = new FormData();

  formData.append('branch_name', branch_name);
  formData.append('address', address);
  formData.append('gen1', gen1);
  formData.append('gen2', gen2);
  formData.append('branch_id', branch_id);

  Swal.fire({
    title: 'PROCCESSING PLEASE WAIT !!!',
    html: '<strong>UPDATING BRANCH..</strong>.', 
    allowOutsideClick: false
  });

  Swal.showLoading();

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
    url: host + update_branch_url,
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
            text: "Successfully Updated Branch.!!",
          });

        }else{
          Swal.close()
          swal({
            title: "Update Failed",
            text: "Please check your values.!!",
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


//////////////////////////////////////////////////////////
///////////////////// UPDATE DEVICES /////////////////////
//////////////////////////////////////////////////////////

let device_forms = document.getElementsByClassName("device");

Array.from(device_forms).forEach((e)=>{

  e.addEventListener("submit", (e)=>{
    e.preventDefault()

    let form_data = e.target.elements;

    let device_name = form_data[0].value;
    let device_id = form_data[1].value;
    let location = form_data[2].value;
    
    let device_pk = e.target.getAttribute('data-device');

    console.log(device_name, device_id, location, device_pk);
    update_device(device_name, device_id, location, device_pk);
    
  })
})

var update_device = ((device_name, device_id, location, device_pk)=>{

  formData = new FormData();

  formData.append('device_name', device_name);
  formData.append('device_pk', device_pk);
  formData.append('location', location);
  formData.append('device_id', device_id);

  Swal.fire({
    title: 'PROCCESSING PLEASE WAIT !!!',
    html: '<strong>UPDATING BRANCH..</strong>.', 
    allowOutsideClick: false
  });

  Swal.showLoading();

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
    url: host + update_device_url,
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
            text: "Successfully Updated Device!!",
          });

        }else{
          Swal.close()
          swal({
            title: "Update Failed",
            text: "Check your values.!!",
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


let add_branch = document.getElementById("new_branch");
let branch = document.getElementsByClassName("branch-object")[0];
let branches_container = document.getElementById("branches-wrapper");
let can_add_new_branch = true;

var create_branch = ((branch_name, address, gen1, gen2, customer_id)=>{

  formData = new FormData();

  formData.append('branch_name', branch_name);
  formData.append('address', address);
  formData.append('gen1', gen1);
  formData.append('gen2', gen2);
  formData.append('customer_id', customer_id);

  Swal.fire({
    title: 'PROCCESSING PLEASE WAIT !!!',
    html: '<strong>CREATING BRANCH..</strong>.', 
    allowOutsideClick: false
  });

  Swal.showLoading();

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
    url: host + create_branch_url,
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
            text: "Successfully Created Branch!!",
          });
          window.location.reload()
        }else{
          Swal.close()
          swal({
            title: "Update Failed",
            text: "Check your values.!!",
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


add_branch.addEventListener("click", (e)=>{
  let branch = `
                <div class="branch-object" id="">
                  <hr style="border: none; border-top: 1px solid #e5e7ee; margin: 0px 0px 15px;">
                    <form id = "new_branch" class="branch" data-branch ="">
                      <div class="grid__row grid__row--margin">
                        <div class="grid__col grid__col--37 grid__col--margin">
                          <label class="form__label">BRANCH NAME</label>
                          <input  class="form__input" type="text" />
                        </div>
                        <div class="grid__col grid__col--37 grid__col--margin">
                          <label class="form__label">BRANCH ADDRESS</label>
                          <input value = "no address" class="form__input" type="text" />
                        </div>
                      </div>
                      <div class="grid__row grid__row--margin">
                        <div class="grid__col grid__col--37 grid__col--margin">
                          <label class="form__label">GENERATOR 1 SIZE (KVA)</label>
                          <input value = "0" class="form__input" type="text" />
                        </div>
                        <div class="grid__col grid__col--37 grid__col--margin">
                          <label class="form__label">GENERATOR 2 SIZE (KVA)</label>
                          <input value = "0" class="form__input" type="text" />
                        </div>
                      </div>
                      <div class="grid__row grid__row--margin">
                        <div class="grid__col grid__col--margin">
                          <input type="submit" class="branch-btn button button--submit button--blue-bg"  value="CREATE BRANCH" style="margin:auto;" />					
                        </div>
                      </div>
                    </form>
                </div>
                `
  if (can_add_new_branch){
    branches_container.insertAdjacentHTML("beforebegin", branch);
  };
  can_add_new_branch = false;

  let new_branch = document.getElementById("new_branch");
  new_branch.addEventListener("submit", (e)=>{
    e.preventDefault();

    let form_data = e.target.elements;

    let branch_name = form_data[0].value;
    let address = form_data[1].value;
    let gen1 = form_data[2].value;
    let gen2 = form_data[3].value;

    console.log(branch_name, address, gen1, gen2, customer_id);

    create_branch(branch_name, address, gen1, gen2, customer_id);
  })
});


var create_device = ((device_name, device_id, location, customer_id, target_branch_id)=>{

  formData = new FormData();

  formData.append('device_name', device_name);
  formData.append('location', location);
  formData.append('device_id', device_id);

  formData.append('customer_id', customer_id);
  formData.append('target_branch_id', target_branch_id);
  console.log(device_name, device_id, location, customer_id, target_branch_id);

  Swal.fire({
    title: 'PROCCESSING PLEASE WAIT !!!',
    html: '<strong>CREATING DEVICE..</strong>.', 
    allowOutsideClick: false
  });

  Swal.showLoading();

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
    url: host + create_device_url,
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
            text: "Successfully Created Device!!",
          });
          window.location.reload()
        }else{
          Swal.close()
          swal({
            title: "Update Failed",
            text: "Check your values.!!",
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

let add_device_btn = document.getElementsByClassName("add_device");
let can_add_new_device = true;

Array.from(add_device_btn).forEach((element)=>{
  element.addEventListener("click", (e)=>{
    e.preventDefault();

    let target_branch_id = e.target.getAttribute('data-branch')
    let target_branch = document.getElementById(`branch-${target_branch_id}`)

    let html_text = `
                      <form class="new_device" data-device ="{{device.id}}" id="device-{{device.id}}" action="">
                      <div class="grid__row grid__row--margin">
                        <div class="grid__col grid__col--37 grid__col--margin">
                          <label class="form__label">DEVICE NAME</label>
                          <input value="no name"  class="form__input" type="text" />
                        </div>
                        <div class="grid__col grid__col--37 grid__col--margin">
                          <label class="form__label">DEVICE ID</label>
                          <input value="111111"  class="form__input" type="text" />
                        </div>
                        <div class="grid__col grid__col--37 grid__col--margin">
                          <label class="form__label">LOCATION</label>
                          <input value="no location set"  class="form__input" type="text" />
                        </div>
                        <div class="grid__col grid__col--37 grid__col--margin">
                          <label class="form__label">DATE ADDED</label>
                          <input style="background-color: #f2f4f8;" none; readonly value="AUTO GENERATED"  class="readonly form__input" type="text" />
                        </div>
                      </div>
                      <div class="grid__row grid__row--margin">
                        <div class="grid__col grid__col--margin">
                          <input  type="submit" class="device button button--submit button--blue-bg"  value="CREATE DEVICE" style="margin:auto;" />					
                        </div>
                      </div>
                    </form>
                    `

    if (can_add_new_device){
      target_branch.insertAdjacentHTML("afterend", html_text);
    };

    can_add_new_device = false;
    let new_device_form = document.getElementsByClassName("new_device");

    Array.from(new_device_form).forEach((e)=>{

      e.addEventListener("submit", (e)=>{
        e.preventDefault();
    
        let form_data = e.target.elements;
    
        let device_name = form_data[0].value;
        let device_id = form_data[1].value;
        let location = form_data[2].value;
    
        // console.log(device_name, device_id, location, customer_id, target_branch_id);
        create_device(device_name, device_id, location, customer_id, target_branch_id);
        
      })
    })
  })
})

