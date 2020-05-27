var host = window.location.hostname == 'localhost'
    ? 'http://localhost:8000/'
    : 'http://' + window.location.hostname + '/'
// console.log(host)

if (location.protocol === 'https:') {
  // page is secure
  host = host.replace("http", "https")
}

var route_to = window.location.href.split("=").length == 1 ? "/" : window.location.href.split("=")[1]; //NEXT PAGE TO REDIRECT TO ON LOGIN 
    
$('#LoginForm').on('submit', async e => {
    e.preventDefault()
    let data = $('#LoginForm') // add lives_in select value to post data
    // console.log(data)
    post()
    
})

const post = ()=>{
  let csrftoken = $('[name="csrfmiddlewaretoken"]')[0].value
  // console.log(csrftoken)
  let page = 'login'

  let form_data = `${$('#LoginForm').serialize()}` // add lives_in select value to post data

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

  $.post(host + 'auth/'+ page , form_data)
        .then(resp => {
          resp = JSON.parse(resp)
          // console.log(resp)
          
          if (resp.response == 'success') {
            window.location.replace(route_to)
          } else if (resp.response == 'failure') {
            $("#login_error").show()
            swal({
              title: "AUTHENTICATION FAILED!!",
              text: "Incorrect Username Or Password..!!",
            });
          }
        })
        .catch(() => {
          text = {
            title: "Network Error",
            text: `Please check your internet connection.!!`,
            icon: "error"
          };
        }) // post data


}