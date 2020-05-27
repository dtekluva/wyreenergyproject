var host = window.location.hostname == 'localhost'
    ? 'http://localhost:8000/'
    : 'http://' + window.location.hostname + '/';

if (location.protocol == 'https:') {
  // page is secure
  host = host.replace("http", "https")
};
    
var endpoint = "fetch_vals_period/";
var usage_difference = "get_yesterday_today_usage/"
var total_kw_endpoint = "get_total_energy/"
var stats_url = "get_stats/"
///////////////////////////////////////////////////////////////////////////
///////////////////                                     ///////////////////
/////////////////  JAVASCRIPT FILTER BY device AND TIME  //////////////////
///////////////////                                     ///////////////////
///////////////////////////////////////////////////////////////////////////

total_kw = document.getElementById("total_kw");
min_kw = document.getElementById("min_kw");
peak_kw = document.getElementById("peak_kw");
avg_kw = document.getElementById("avg_kw");
today_usage = document.getElementById("today_usage");

yesterday_usage = document.getElementById("yesterday_usage");
increase_today = document.getElementById("increase_today");
decrease_today = document.getElementById("decrease_today");
increase_yesterday = document.getElementById("increase_yesterday");
decrease_yesterday = document.getElementById("decrease_yesterday");


$(window).on('load', function() {
  fetch_reading();
});

$('#time_period').on('apply.daterangepicker', async e => {
  fetch_reading();
});

$('#load_readings').on('click', async e => {
  fetch_reading();
});

var fetch_reading = (()=>{

  let devices = get_selected_devices();
  let period = $("#time_period")[0].value;

  if (Boolean(devices.length)){
    get_usage_difference(devices);
    get_kwh(devices, period);
    get_stats(devices, period);
    load_charts(devices, period);
  }
  else{
    swal({
      title: "No Devices Selected!!",
      text: "Try selecting a devices/devices first and try again",
    });
  };
})

const get_kwh = (device, period)=>{
  let csrftoken = $('[name="csrfmiddlewaretoken"]')[0].value

  let data = {
              "device": device,
              "period": period
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
  
  $.post(host + total_kw_endpoint, data)
        .then(resp => {
          resp = JSON.parse(resp)
          console.log(resp);
          if (resp.response == 'success') {
              // alert("Feature in progress");
              total_kw.innerHTML = `${resp.data} kWh`;

          } else if (resp.response == 'failure') {
            swal({
                  title: "Error fetching data!!",
                  text: "Try selecting a valid date range first",
                });
          }
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
        }) // post data
};

const get_stats = (device, period)=>{ //GET MIN MAX AND AVERAGE VALUES

  let csrftoken = $('[name="csrfmiddlewaretoken"]')[0].value

  let data = {
              "device": device,
              "period": period
              };
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
  
  $.post(host + stats_url, data)
        .then(resp => {
          resp = JSON.parse(resp)
          console.log(resp);
          if (resp.response == 'success') {
              avg_kw.innerHTML = Math.floor(resp.data.avg);
              min_kw.innerHTML = Math.floor(resp.data.min);
              peak_kw.innerHTML = Math.floor(resp.data.max);
              
          } else if (resp.response == 'failure') {
            swal({
                  title: "Error fetching data!!",
                  text: "Try selecting a valid date range first",
                });
          }
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
        }) // post data
};

const get_usage_difference = (devices)=>{
  let csrftoken = $('[name="csrfmiddlewaretoken"]')[0].value
  // console.log(period)

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
  let data = {
    "devices": devices
    };
  data = JSON.stringify(data);
  
  $.post(host + usage_difference, data)
        .then(resp => {
          resp = JSON.parse(resp)
          console.log(resp);

          if (resp.response == 'success') {

            yesterday_usage.innerHTML = resp.data.yesterday_energy;
            today_usage.innerHTML = resp.data.today_energy;

            if (resp.data.yesterday_energy > resp.data.today_energy){
              increase_yesterday.className = "arrow_up"
              increase_today.className = "arrow_up hide"
              decrease_yesterday.className = "arrow_up hide"
              decrease_today.className = "arrow_up"
            }
            else if (resp.data.yesterday_energy < resp.data.today_energy){
              increase_yesterday.className = "arrow_up hide"
              increase_today.className = "arrow_up"
              decrease_yesterday.className = "arrow_up"
              decrease_today.className = "arrow_up hide"
            }
            else if(resp.data.yesterday_energy > resp.data.today_energy){

            }

          } else if (resp.response == 'failure') {
            swal({
                  title: "Error fetching data!!",
                  text: "An error occurred",
                });
          }
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
        }) // post data
}

const load_charts = (device, period)=>{
  let csrftoken = $('[name="csrfmiddlewaretoken"]')[0].value
  // console.log(period)

  let data = {
              "device": device,
              "period": period
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
  
  $.post(host + endpoint, data)
        .then(resp => {
          resp = JSON.parse(resp)
          console.log(resp);
          if (resp.response == 'success') {
              // alert("Feature in progress");
              days = resp.data.daily_device_usage.days;
              utility = resp.data.daily_device_usage.utility;
              gen1 = resp.data.daily_device_usage.gen1;
              gen2 = resp.data.daily_device_usage.gen2;
              utility_hrs = resp.data.utility_times;
              gen1_hrs = resp.data.gen1_times;
              gen2_hrs = resp.data.gen2_times;
              addData(DiseasesChart, utility_hrs, gen1_hrs, gen2_hrs);
              update_bar_chart(ActivityChart, days, utility, gen1, gen2);                
              
              // if (endpoint == "fetch_vals_period/"){
              //     addData(DiseasesChart, utility_hrs, gen1_hrs, gen2_hrs); 
              // }else{
              //   update_bar_chart(ActivityChart, days, utility, gen1, gen2);
              // };

              // endpoint = "fetch_device_vals/";
            
          } else if (resp.response == 'failure') {
            swal({
                  title: "Error fetching data!!",
                  text: "Try selecting a valid date range first",
                });
          }
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
        }) // post data
};

function addData(chart, utility, gen1, gen2) {
  chart.data.datasets.forEach((dataset) => {
      dataset.data = [gen1, gen2, utility];
  });
  chart.update();
}

function update_bar_chart(chart, days, utility, gen1, gen2) {
  chart.data.labels = days;
  chart.data.datasets[0].data = utility;
  chart.data.datasets[1].data = gen1;
  chart.data.datasets[2].data = gen2;
  chart.update();
}

function sum(input){
             
  if (toString.call(input) !== "[object Array]")
     return false;
       
             var total =  0;
             for(var i=0;i<input.length;i++)
               {                  
                 if(isNaN(input[i])){
                 continue;
                  }
                   total += Number(input[i]);
                }
              return total;
             }


var expanded = false;
  function showCheckboxes() {
    
    if (!expanded) {
      checkboxes.style.display = "block";
      expanded = true;
    } else {
      checkboxes.style.display = "none";
      expanded = false;
  }
};

const get_selected_devices = (()=>{
  let device_checkboxes = document.getElementsByClassName("device_checkbox");

  let checked_devices = Array.from(device_checkboxes).filter((e)=>{
    return e.checked == true
  });

  let device_ids = checked_devices.map(element => element.id)

  return device_ids
});














// var host = window.location.hostname == 'localhost'
//     ? 'http://localhost:8000/'
//     : 'http://' + window.location.hostname + '/';

// if (location.protocol == 'https:') {
//   // page is secure
//   host = host.replace("http", "https")
// };
    
// var endpoint = "fetch_vals_period/";
// var usage_difference = "get_yesterday_today_usage/"
// ///////////////////////////////////////////////////////////////////////////
// ///////////////////                                     ///////////////////
// /////////////////  JAVASCRIPT FILTER BY device AND TIME  //////////////////
// ///////////////////                                     ///////////////////
// ///////////////////////////////////////////////////////////////////////////

// total_kw = document.getElementById("total_kw");
// min_kw = document.getElementById("min_kw");
// peak_kw = document.getElementById("peak_kw");
// avg_kw = document.getElementById("avg_kw");
// today_usage = document.getElementById("today_usage");

// yesterday_usage = document.getElementById("yesterday_usage");
// increase_today = document.getElementById("increase_today");
// decrease_today = document.getElementById("decrease_today");
// increase_yesterday = document.getElementById("increase_yesterday");
// decrease_yesterday = document.getElementById("decrease_yesterday");


// $(window).on('load', function() {
//   let device = $("#device")[0].value;
//   // console.log(device)
//   let period = $("#default_range")[0].innerHTML;
//   get_usage_difference("None");
//   post(device, period);
// });
    
// $('#device').on('change', async e => {
//     let device = $("#device")[0].value;
//     let period = $("#time_period")[0].value;
//     get_usage_difference(device);
//     post(device, period);
// });

// $('#time_period').on('apply.daterangepicker', async e => {
//     let device = $("#device")[0].value;
//     let period = $("#time_period")[0].value;
//     post(device, period);
// });

// const post = (device, period)=>{
//   let csrftoken = $('[name="csrfmiddlewaretoken"]')[0].value
//   // console.log(period)

//   let data = {
//               "device": device,
//               "period": period
//               }; // add lives_in select value to post data

//   function csrfSafeMethod (method) {
//         // these HTTP methods do not require CSRF protection
//     return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
//   }

//   $.ajaxSetup({
//     beforeSend: function (xhr, settings) {
//       if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//         xhr.setRequestHeader('X-CSRFToken', csrftoken)
//       }
//     }
//   })
  
//   $.post(host + endpoint, data)
//         .then(resp => {
//           resp = JSON.parse(resp)
//           console.log(resp);
//           if (resp.response == 'success') {
//               // alert("Feature in progress");
//               total_kw.innerHTML = `${resp.data.energy_used} kwh`;
//               peak_kw.innerHTML = resp.data.peak_kw;
//               min_kw.innerHTML = resp.data.min_kw;
//               avg_kw.innerHTML = resp.data.avg_kw;
//               days = resp.data.daily_device_usage.days;
//               utility = resp.data.daily_device_usage.utility;
//               gen1 = resp.data.daily_device_usage.gen1;
//               gen2 = resp.data.daily_device_usage.gen2;
//               utility_hrs = resp.data.utility_times;
//               gen1_hrs = resp.data.gen1_times;
//               gen2_hrs = resp.data.gen2_times;
//               addData(DiseasesChart, utility_hrs, gen1_hrs, gen2_hrs);
              
//               if (endpoint == "fetch_vals_period/"){
//                   addData(DiseasesChart, utility_hrs, gen1_hrs, gen2_hrs); 
//                   update_bar_chart(ActivityChart, days, utility, gen1, gen2);                
//               }else{
//                 update_bar_chart(ActivityChart, days, utility, gen1, gen2);
//               };

//               endpoint = "fetch_device_vals/";
            
//           } else if (resp.response == 'failure') {
//             swal({
//                   title: "Error fetching data!!",
//                   text: "Try selecting a valid date range first",
//                 });
//           }
//         })
//         .catch(() => {
//           text = {
//             title: "Network Error",
//             text: `Please check your internet connection.!!`,
//             icon: "error"
//           };
//           swal({
//             title: "Network Error",
//             text: "Please check your internet connection.!!",
//           });
//         }) // post data
// };

// const get_usage_difference = (device)=>{
//   let csrftoken = $('[name="csrfmiddlewaretoken"]')[0].value
//   // console.log(period)

//   function csrfSafeMethod (method) {
//         // these HTTP methods do not require CSRF protection
//     return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
//   }

//   $.ajaxSetup({
//     beforeSend: function (xhr, settings) {
//       if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//         xhr.setRequestHeader('X-CSRFToken', csrftoken)
//       }
//     }
//   })
//   let data = {
//     "device": device
//     };
  
//   $.post(host + usage_difference, data)
//         .then(resp => {
//           resp = JSON.parse(resp)
//           console.log(resp);

//           if (resp.response == 'success') {

//             yesterday_usage.innerHTML = resp.data.yesterday_energy;
//             today_usage.innerHTML = resp.data.today_energy;

//             if (resp.data.yesterday_energy > resp.data.today_energy){
//               increase_yesterday.className = "arrow_up"
//               increase_today.className = "arrow_up hide"
//               decrease_yesterday.className = "arrow_up hide"
//               decrease_today.className = "arrow_up"
//             }
//             else if (resp.data.yesterday_energy < resp.data.today_energy){
//               increase_yesterday.className = "arrow_up hide"
//               increase_today.className = "arrow_up"
//               decrease_yesterday.className = "arrow_up"
//               decrease_today.className = "arrow_up hide"
//             }
//             else if(resp.data.yesterday_energy > resp.data.today_energy){

//             }

//           } else if (resp.response == 'failure') {
//             swal({
//                   title: "Error fetching data!!",
//                   text: "An error occurred",
//                 });
//           }
//         })
//         .catch(() => {
//           text = {
//             title: "Network Error",
//             text: `Please check your internet connection.!!`,
//             icon: "error"
//           };
//           swal({
//             title: "Network Error",
//             text: "Please check your internet connection.!!",
//           });
//         }) // post data
// }


// function addData(chart, utility, gen1, gen2) {
//   chart.data.datasets.forEach((dataset) => {
//       dataset.data = [gen1, gen2, utility];
//   });
//   chart.update();
// }

// function update_bar_chart(chart, days, utility, gen1, gen2) {
//   chart.data.labels = days;
//   chart.data.datasets[0].data = utility;
//   chart.data.datasets[1].data = gen1;
//   chart.data.datasets[2].data = gen2;
//   chart.update();
// }

// function sum(input){
             
//   if (toString.call(input) !== "[object Array]")
//      return false;
       
//              var total =  0;
//              for(var i=0;i<input.length;i++)
//                {                  
//                  if(isNaN(input[i])){
//                  continue;
//                   }
//                    total += Number(input[i]);
//                 }
//               return total;
//              }


// var expanded = false;
//   function showCheckboxes() {
    
//     if (!expanded) {
//       checkboxes.style.display = "block";
//       expanded = true;
//     } else {
//       checkboxes.style.display = "none";
//       expanded = false;
//       selected_devices = get_selected_devices();
//       console.log(selected_devices);
//   }
// };

// const get_selected_devices = (()=>{
//   let device_checkboxes = document.getElementsByClassName("device_checkbox");

//   let checked_devices = Array.from(device_checkboxes).filter((e)=>{
//     return e.checked == true
//   });

//   let device_ids = checked_devices.map(element => element.id)

//   return device_ids
// });