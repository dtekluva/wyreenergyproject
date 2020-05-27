var host = window.location.hostname == 'localhost'
    ? 'http://localhost:8000/'
    : 'http://' + window.location.hostname + '/';

if (location.protocol === 'https:') {
  // page is secure
  host = host.replace("http", "https")
}
    
var endpoint = "get_last_read/";
///////////////////////////////////////////////////////////////////////////
///////////////////                                     ///////////////////
/////////////////  JAVASCRIPT FILTER BY device AND TIME  //////////////////
///////////////////                                     ///////////////////
///////////////////////////////////////////////////////////////////////////

total_kw = document.getElementById("total_kw")
var time_span = document.getElementById("update_time")


$(window).on('load', function() {
  let device = $("#device")[0].value;
  post(device);
})
    
$('#device').on('change', async e => {
    let device = $("#device")[0].value
    post(device);
})

const post = (device)=>{
  let csrftoken = $('[name="csrfmiddlewaretoken"]')[0].value

  let data = {
              "device": device
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
          // console.log(resp);
          if (resp.response == 'success') {
            
              populate(resp);
              endpoint = "get_last_read/";
            
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

function populate(_data){
  console.log(_data);
  time_span.innerHTML = new Date(_data.data.record_time);
  
  document.getElementById("vl1").innerHTML = _data.data.voltage_l1_l12.value || '-';
  document.getElementById("vl2").innerHTML = _data.data.voltage_l2_l23.value || '-';
  document.getElementById("vl3").innerHTML = _data.data.voltage_l3_l31.value || '-';
  document.getElementById("amp_l1").innerHTML = _data.data.current_l1.value || '-';
  document.getElementById("amp_l2").innerHTML = _data.data.current_l2.value || '-';
  document.getElementById("amp_l3").innerHTML = _data.data.current_l3.value || '-';
  document.getElementById("active_kw_l1").innerHTML = _data.data.kw_l1.value || '-';
  document.getElementById("active_kw_l2").innerHTML = _data.data.kw_l2.value || '-';
  document.getElementById("active_kw_l3").innerHTML = _data.data.kw_l3.value || '-';
  document.getElementById("active_kv_l1").innerHTML = _data.data.kva_l1.value || '-';
  document.getElementById("active_kv_l2").innerHTML = _data.data.kva_l2.value || '-';
  document.getElementById("active_kv_l3").innerHTML = _data.data.kva_l3.value || '-';
  document.getElementById("active_kvar_l1").innerHTML = _data.data.kvar_l1.value || '-';
  document.getElementById("active_kvar_l2").innerHTML = _data.data.kvar_l2.value || '-';
  document.getElementById("active_kvar_l3").innerHTML = _data.data.kvar_l3.value || '-';
  document.getElementById("pf_l1").innerHTML = _data.data.power_factor_l1.value || '-';
  document.getElementById("pf_l2").innerHTML = _data.data.power_factor_l2.value || '-';
  document.getElementById("pf_l3").innerHTML = _data.data.power_factor_l3.value || '-';
  document.getElementById("kw_tot").innerHTML = _data.data.total_kw.value || '-';
  document.getElementById("kvar_tot").innerHTML = _data.data.total_kvar.value || '-';
  document.getElementById("kva_tot").innerHTML = _data.data.total_kva.value || '-';
  document.getElementById("pf_tot").innerHTML = _data.data.total_pf.value || '-';
  document.getElementById("frequency").innerHTML = _data.data.avg_frequency.value || '-';
  document.getElementById("neutral_current").innerHTML = _data.data.neutral_current.value || '-';
  document.getElementById("voltage_thd_l1").innerHTML = _data.data.volt_thd_l1_l12.value || '-';
  document.getElementById("voltage_thd_l2").innerHTML = _data.data.volt_thd_l2_l23.value || '-';
  document.getElementById("voltage_thd_l3").innerHTML = _data.data.volt_thd_l3_l31.value || '-';
  document.getElementById("current_thd_l1").innerHTML = _data.data.current_thd_l1.value || '-';
  document.getElementById("current_thd_l2").innerHTML = _data.data.current_thd_l2.value || '-';
  document.getElementById("current_thd_l3").innerHTML = _data.data.current_thd_l3.value || '-';
  document.getElementById("current_tdd_l1").innerHTML = _data.data.current_tdd_l1.value || '-';
  document.getElementById("current_tdd_l2").innerHTML = _data.data.current_tdd_l2.value || '-';
  document.getElementById("current_tdd_l3").innerHTML = _data.data.current_tdd_l3.value || '-';
  document.getElementById("kwh_import").innerHTML = _data.data.kwh_import.value || '-';
  document.getElementById("kwh_export").innerHTML = _data.data.kwh_export.value || '-';
  document.getElementById("kvarh_import").innerHTML = _data.data.kvarh_import.value || '-';
  document.getElementById("kvah_total").innerHTML = _data.data.kvah_total.value || '-';
  document.getElementById("max_amp_demand_l1").innerHTML = _data.data.max_amp_demand_l1.value || '-';
  document.getElementById("max_amp_demand_l2").innerHTML = _data.data.max_amp_demand_l2.value || '-';
  document.getElementById("max_amp_demand_l3").innerHTML = _data.data.max_amp_demand_l3.value || '-';
  document.getElementById("max_sliding_window_kw_demand").innerHTML = _data.data.max_sliding_window_kw_demand.value || '-';
  document.getElementById("accum_kw_demand").innerHTML = _data.data.accum_kw_demand.value || '-';
  document.getElementById("max_sliding_window_kva_demand").innerHTML = _data.data.max_sliding_window_kva_demand.value || '-';
  document.getElementById("present_sliding_window_kw_demand").innerHTML = _data.data.present_sliding_window_kw_demand.value || '-';
  document.getElementById("present_sliding_window_kva_demand").innerHTML = _data.data.present_sliding_window_kva_demand.value || '-';
  document.getElementById("accum_kva_demand").innerHTML = _data.data.accum_kva_demand.value || '-';
  document.getElementById("pf_import_at_maximum_kva_sliding_window_demand").innerHTML = _data.data.pf_import_at_maximum_kva_sliding_window_demand.value || '-';
}

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
