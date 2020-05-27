var host = window.location.hostname == 'localhost'
    ? 'http://localhost:8000/'
    : 'http://' + window.location.hostname + '/';

if (location.protocol === 'https:') {
  // page is secure
  host = host.replace("http", "https")
}
    
const endpoint = "get_line_readings/";
const logs_url = "get_line_readings_log/";
var table;
var values = {"data":{}}
///////////////////////////////////////////////////////////////////////////
///////////////////                                     ///////////////////
/////////////////  JAVASCRIPT FILTER BY device AND TIME  //////////////////
///////////////////                                     ///////////////////
///////////////////////////////////////////////////////////////////////////

device = document.getElementById("device")
parameter = document.getElementById("parameter")
_date = document.getElementById("single_date")
// let period = $("#time_period")[0].value
    
$('#device').on('change', async e => {
  let device = $("#device")[0].value;
  let period = $("#read_time_period")[0].value

  post(device);
  get_logs(device, period);
})

$('#parameter').on('change', async e => {
  let device = $("#device")[0].value;
  post(device);
})

//LOAD DATE RANGE PICKER
$('#read_time_period').on('apply.daterangepicker', async e => {
  let device = $("#device")[0].value
  let period = $("#read_time_period")[0].value
  get_logs(device, period);
})

//LOAD DATE PICKER
$(function() {
  $('input[name="date"]').daterangepicker({
    singleDatePicker: true,
    showDropdowns: true,
    "minYear": 2017,
    "maxYear": 2025,
    "startDate": todays_date,
    onSelect: function() {
      $(this).data('datepicker').inline = true;                               
  }
  });
});

//LOAD DATEPICKER ONCHANGE EVENT
$('input[name="date"]').on('apply.daterangepicker', async e => {
  let device = $("#device")[0].value
  post(device);
})
$(document).ready(function() {
  
} );

$(window).on('load', function() {

  let device = $("#device")[0].value;
  let period = $("#default_range")[0].innerHTML;

  table = $('#reaing_table').DataTable( {
                "scrollX": true,
                dom: 'Bfrtip',
                buttons: [
                    'copy', 'csv', 'excel', 'pdf', '# print'
                    
                ],
                "columnDefs": [
                  {"className": "dt-center", "targets": "_all"}
                ],
                "pageLength": 20
              } );
  post(device);
  get_logs(device, period);
});

const post = (device)=>{
  let csrftoken = $('[name="csrfmiddlewaretoken"]')[0].value
  let data = {
              "device": device,
              "date": _date.value
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
  
  $.post(host + endpoint, data)
        .then(resp => {
          resp = JSON.parse(resp)
          values.data = resp.data;
          
          if (resp.response == 'success') {
            
            if (parameter.value == "Voltage (Volts)"){
              table.clear().draw(); 

              populate_voltage(prepare_data_voltage());
            }
            else if(parameter.value == "Current (Amps)"){

              populate_current(prepare_data_current());
            } 
            else if(parameter.value == "Active-Power (kW)"){

              populate_active_power(prepare_data_active_power());
            } 
            else if(parameter.value == "Reactive-Power (kVAR)"){

              populate_reactive_power(prepare_data_reactive_power());
            } 
            else if(parameter.value == "Energy (kWh)"){

              populate_energy(prepare_data_energy());
            } 
            
          } else if (resp.response == 'failure') {
            swal({
                  title: "Error fetching data!!",
                  text: "Something went wrong",
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

const get_logs = (device, period)=>{
  let csrftoken = $('[name="csrfmiddlewaretoken"]')[0].value
  // console.log(period)

  let data = {
              "device": device,
              "period": period
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

  Swal.fire({
    title: 'PROCCESSING PLEASE WAIT !!!',
    html: '<strong>FETCHING READINGS FOR SELECTED PERIOD</strong>.', 
    allowOutsideClick: false
  });
  Swal.showLoading();
  
  $.post(host + logs_url, data)
        .then(resp => {
          resp = JSON.parse(resp)
          
          Swal.getContent().querySelector('strong')
            .textContent = `LOADED ${resp.data.length} READINGS, RENDERING VALUES.`
          
          return resp;
        })
        .then(resp=> {
          if (resp.response == 'success') {
            if (resp.data.length < 1){
              Swal.close()
            }
            setTimeout(() => {
              add_to_tables(resp);
            }, 1000);
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
}

function populate_current(data){
    
    ActivityChart.chart.data.datasets[0].data = data.l1
    ActivityChart.chart.data.datasets[0].label = "Amps(L1)"
    ActivityChart.chart.data.datasets[1].data = data.l2
    ActivityChart.chart.data.datasets[1].label = "Amps(L2)"
    ActivityChart.chart.data.datasets[2].data = data.l3
    ActivityChart.chart.data.datasets[2].label = "Amps(L3)"
    ActivityChart.chart.data.datasets[3].data = data.neutral
    ActivityChart.chart.data.datasets[3].label = "Amps(Neutral)"
    ActivityChart.chart.data.labels = data.time
    ActivityChart.update();
}

function prepare_data_current(){
  let _time = [];
  let l1 = [];
  let l2 = [];
  let l3 = [];
  let neutral = [];

  values.data.forEach(element => {
    _time.push(time_convert(element.post_time))
    l1.push(element.current_l1)
    l2.push(element.current_l2)
    l3.push(element.current_l3)
    neutral.push(element.neutral_current)
  });

  return {'time':_time,'l1':l1,'l2':l2, 'l3':l3, 'neutral':neutral}
};

function populate_voltage(data){
 
    
  ActivityChart.chart.data.datasets[0].data = data.l1
  ActivityChart.chart.data.datasets[0].label = "Volts(L1)"
  ActivityChart.chart.data.datasets[1].data = data.l2
  ActivityChart.chart.data.datasets[1].label = "Volts(L2)"
  ActivityChart.chart.data.datasets[2].data = data.l3
  ActivityChart.chart.data.datasets[2].label = "Volts(L3)"
  ActivityChart.chart.data.datasets[3].data = data.hz
  ActivityChart.chart.data.datasets[3].label = "Frequency"
  ActivityChart.chart.data.labels = data.time
  ActivityChart.update();

}

function prepare_data_voltage(){
  let _time = [];
  let l1 = [];
  let l2 = [];
  let l3 = [];
  let hz = [];

  values.data.forEach(element => {
    _time.push(time_convert(element.post_time))
    l1.push(element.voltage_l1_l12)
    l2.push(element.voltage_l2_l23)
    l3.push(element.voltage_l3_l31)
    hz.push(element.avg_frequency)
  });

  return {'time':_time,'l1':l1,'l2':l2, 'l3':l3, 'hz':hz}
};

function populate_active_power(data){
    
  ActivityChart.chart.data.datasets[0].data = data.l1
  ActivityChart.chart.data.datasets[0].label = "K-Watts(L1)"
  ActivityChart.chart.data.datasets[1].data = data.l2
  ActivityChart.chart.data.datasets[1].label = "K-Watts(L2)"
  ActivityChart.chart.data.datasets[2].data = data.l3
  ActivityChart.chart.data.datasets[2].label = "K-Watts(L3)"
  ActivityChart.chart.data.datasets[3].data = data.hz
  ActivityChart.chart.data.datasets[3].label = "Frequency"
  ActivityChart.chart.data.labels = data.time
  ActivityChart.update();

}

function prepare_data_active_power(){
  let _time = [];
  let l1 = [];
  let l2 = [];
  let l3 = [];
  let hz = [];

  values.data.forEach(element => {
    _time.push(time_convert(element.post_time))
    l1.push(element.kw_l1)
    l2.push(element.kw_l2)
    l3.push(element.kw_l3)
    hz.push(element.avg_frequency)
  });

  return {'time':_time,'l1':l1,'l2':l2, 'l3':l3, 'hz':hz}
};

function populate_reactive_power(data){
    
  ActivityChart.chart.data.datasets[0].data = data.l1
  ActivityChart.chart.data.datasets[0].label = "K-VAR (L1)"
  ActivityChart.chart.data.datasets[1].data = data.l2
  ActivityChart.chart.data.datasets[1].label = "K-VAR (L2)"
  ActivityChart.chart.data.datasets[2].data = data.l3
  ActivityChart.chart.data.datasets[2].label = "K-VAR (L3)"
  ActivityChart.chart.data.datasets[3].data = data.hz
  ActivityChart.chart.data.datasets[3].label = "Frequency"
  ActivityChart.chart.data.labels = data.time
  ActivityChart.update();

};

function prepare_data_reactive_power(){
  let _time = [];
  let l1 = [];
  let l2 = [];
  let l3 = [];
  let hz = [];

  values.data.forEach(element => {
    _time.push(time_convert(element.post_time))
    l1.push(element.kvar_l1)
    l2.push(element.kvar_l2)
    l3.push(element.kvar_l3)
    hz.push(element.avg_frequency)
  });

  return {'time':_time,'l1':l1,'l2':l2, 'l3':l3, 'hz':hz}
};

function populate_energy(data){
    
  ActivityChart.chart.data.datasets[0].data = data.energy
  ActivityChart.chart.data.datasets[0].label = "Energy Usage (kWh)"
  ActivityChart.chart.data.datasets[1].data = data.l2
  ActivityChart.chart.data.datasets[1].label = "-"
  ActivityChart.chart.data.datasets[2].data = data.l3
  ActivityChart.chart.data.datasets[2].label = "-"
  ActivityChart.chart.data.datasets[3].data = data.hz
  ActivityChart.chart.data.datasets[3].label = "-"
  ActivityChart.chart.data.labels = data.time
  ActivityChart.update();

}

function prepare_data_energy(){
  let _time = [];
  let energy = [];
  let l2 = [];
  let l3 = [];
  let hz = [];
  
  let start_energy_val = values.data.length > 0 ?  values.data[0].kwh_import : 0;

  values.data.forEach(element => {
    _time.push(time_convert(element.post_time))
    energy.push(element.kwh_import - start_energy_val);
  });

  return {'time':_time,'energy':energy,'l2':l2, 'l3':l3, 'hz':hz}
};

function time_convert (time) {
  // Check correct time format and split into components
  time = time.slice(0,8)
  time = time.toString().match (/^([01]\d|2[0-3])(:)([0-5]\d)(:[0-5]\d)?$/) || [time];

  if (time.length > 1) { // If time format correct
    time = time.slice(1);  // Remove full string match value
    time[5] = +time[0] < 12 ? 'AM' : 'PM'; // Set AM/PM
    time[0] = +time[0] % 12 || 12; // Adjust hours
  }
  return time.join (''); // return adjusted time or original string
}

function add_to_tables(readings){
  table.clear().draw()
  readings.data.forEach(element => {
    table.row.add( [
      element.post_datetime,
      element.voltage_l1_l12,
      element.voltage_l2_l23,
      element.voltage_l3_l31,
      element.current_l1,
      element.current_l2,
      element.current_l3,
      element.kw_l1,
      element.kw_l2,
      element.kw_l3,
      element.kvar_l1,
      element.kvar_l2,
      element.kvar_l3,
      element.power_factor_l1,
      element.power_factor_l2,
      element.power_factor_l3,
      element.avg_frequency
  ] )
  Swal.close()
});
    
 table.draw();
};

function todays_date(){
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
  var yyyy = today.getFullYear();

  today = mm + '/' + dd + '/' + yyyy;
  return today
}

// ADD THE ABILITY TO REMOVE ONE HOUR FROM A TIME OBJECT TO JS TIME CLASS
Date.prototype.remHours = function(h) {  
  this.setTime(this.getTime() - (h*60*60*1000));
  return this;
}
