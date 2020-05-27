var host = window.location.hostname == 'localhost'
    ? 'http://localhost:8000/'
    : 'http://' + window.location.hostname + '/'

if (location.protocol === 'https:') {
  // page is secure
  host = host.replace("http", "https")
}
  
const endpoint = "fetch_messages/";
const message_url = "send_message/";
var message_box = document.getElementsByClassName("conversation")
var downloaded_messages = [] ;


$(window).on('load', function() {
  let conversations = document.getElementById("message_list");
  
  conversations.addEventListener("click", (e)=>{
    // console.log(conversations.children[0].className);
    // if (e.target.className == "messages__short-name"){
    //   return
    // }
    console.log(e.target.className);
    let customer_name = e.srcElement.innerText;
    let customer_img = e.srcElement.childNodes[1].childNodes[0].currentSrc;
    console.log(e.srcElement);
    let customer_name_div = document.getElementsByClassName("messages__header-user")[0];
    customer_name_div.innerHTML = customer_name;
  
    let customer_img_div = document.getElementsByClassName("messages__header-thumb")[0].firstChild;
    customer_img_div.src = customer_img;
    populate_messages();  
    
  })

  let customer_id = conversations.children[0].id;
  let customer_name = conversations.children[0].childNodes[1].innerText;
  let customer_img = conversations.children[0].childNodes[1].firstElementChild.children[0].currentSrc;

  let customer_name_div = document.getElementsByClassName("messages__header-user")[0];
  customer_name_div.innerHTML = customer_name;

  let customer_img_div = document.getElementsByClassName("messages__header-thumb")[0].firstChild;
  console.dir(customer_img_div);
  customer_img_div.src = customer_img;


  console.log(customer_img);
  conversations.children[0].className += " selected";
  console.log(conversations.children[0].className);
  post(customer_id);  
  activate_message_btn();
});
    
const post = (customer_id)=>{
  let csrftoken = $('[name="csrfmiddlewaretoken"]')[0].value

  let data = {
              "customer_id": customer_id,
              }; // add lives_in select value to post data

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
  $.post(host + endpoint)
        .then(resp => {
          resp = JSON.parse(resp)
          
          if (resp.response == 'success') {
              // alert("Feature in progress");
              
                
          }else if (resp.response == 'failure') {
            swal({
                  title: "Error fetching data!!",
                  text: "Try selecting a valid date range first",
                });
          }
          return resp;
        })
        .then(resp => {
          let active_chat_user = document.getElementsByClassName("messages__header-user")
          window.downloaded_messages = resp;
          return resp
        }).then((resp)=>{
          populate_messages(resp)
        })
        .catch(() => {
          text = {
            title: "Network Error",
            text: `Please check your internet connection.!!`,
            icon: "error"
          };
          swal({
            title: "Network Error",
            text: "Please check your internet connection.!!",
          });
        })

  setInterval(() => {
    $.post(host + endpoint)
        .then(resp => {
          resp = JSON.parse(resp)
          
          if (resp.response == 'success') {
              // alert("Feature in progress");
              
                
          }else if (resp.response == 'failure') {
            swal({
                  title: "Error fetching data!!",
                  text: "Try selecting a valid date range first",
                });
          }
          return resp;
        })
        .then(resp => {
          window.downloaded_messages = resp;
          return resp
        }).then((resp)=>{
          populate_messages(resp)
        })
        .catch(() => {
          text = {
            title: "Network Error",
            text: `Please check your internet connection.!!`,
            icon: "error"
          };
          swal({
            title: "Network Error",
            text: "Please check your internet connection.!!",
          });
        })
  }, 10000); 
};

var is_first_load = true;

var populate_messages = (()=>{
    let customer_id = document.getElementsByClassName("selected")[0].id;
    let values = downloaded_messages.data[customer_id]
    // console.log(downloaded_messages);
    text = ""
    values.forEach(element => {
      if (!element.outgoing){
        text += `<li class="conversation__row conversation__row--received">
                    <div class="conversation__avatar"></div>
                    
                    <div class="conversation__content">
                      <p>${element.content} </p>
                    <span class="conversation__time">${element.time}</span>
                    </div>
                    
                </li>`
      }
      else{
        text += `<li class="conversation__row conversation__row--sent">
                    <div class="conversation__avatar"></div>
                    
                    <div class="conversation__content">
                      <p>${element.content} </p>
                    <span class="conversation__time">${element.time}</span>
                    </div>
                    
                </li>`
      }

    });
    var message_box = document.getElementsByClassName("conversation")[0]
    message_box.innerHTML = text;
    var messages = document.getElementsByClassName("conversation__row");
    if (is_first_load){
      messages[messages.length - 1].scrollIntoView();
    }
    is_first_load = false;
})

var activate_message_btn = (()=>{
  
  let message_icon = document.getElementById("submit_icon");
  
  message_icon.addEventListener("click", ((e)=>{

    let customer_id = document.getElementsByClassName("selected")[0].id;
    e.preventDefault();
    let text = document.getElementById("message_input").value;
    console.log(text)
    post_message(customer_id, text)
  }))
});

const post_message = (customer_id, text)=>{
  let csrftoken = $('[name="csrfmiddlewaretoken"]')[0].value

  let data = {
              "customer_id": customer_id,
              "text": text
              }; // add lives_in select value to post data
  data = JSON.stringify(data);

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
  $.post(host + message_url, data)
        .then(resp => {
          resp = JSON.parse(resp)
          
          if (resp.response == 'success') {
              // alert("Feature in progress");
              window.downloaded_messages = resp;
                
          }else if (resp.response == 'failure') {
            swal({
                  title: "Error fetching data!!",
                  text: "Try selecting a valid date range first",
                });
          }
          return resp;
        })
        .then(resp => {
          populate_messages()
          let text = document.getElementById("message_input")
          
          text.value = "";
        })
        .catch(() => {
          text = {
            title: "Network Error",
            text: `Please check your internet connection.!!`,
            icon: "error"
          };
          swal({
            title: "Network Error",
            text: "Please check your internet connection.!!",
          });
        })
};