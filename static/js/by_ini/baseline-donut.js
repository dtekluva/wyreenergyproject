var host = window.location.hostname == 'localhost'
    ? 'http://localhost:8000/'
    : 'http://' + window.location.hostname + '/';

if (location.protocol == 'https:') {
  // page is secure
  host = host.replace("http", "https")
};
    
const endpoint = "get_capacity_factors/";
var baseline_chart;
var table;
var values = {"data":{}}

let historyButtons = document.querySelectorAll("a.history-button");
let historyModal = document.querySelector("div.history-modal-container");
let cardsContainer = document.querySelector("div.cards-container");
let sidebarSection = document.querySelector("div.section--sidebar");
let sidebarHeader = document.querySelector("header.sidebar-header");
let contentHeader = document.querySelector("header.content-header");
let contentSubheader = document.querySelector("div.content-subheader");
let panelSection = document.querySelector("div.section-panel");
let otherModals = document.querySelector("div.modal");


///////////////////////////////////////////////////////////////////////////
///////////////////                                     ///////////////////
/////////////////  JAVASCRIPT FILTER BY device AND TIME  //////////////////
///////////////////                                     ///////////////////
///////////////////////////////////////////////////////////////////////////

$(window).on('load', ()=> {
  let device = $("#device")[0].value;
  load_baseline();
})
const load_baseline = (device, period)=>{
  let csrftoken = $('[name="csrfmiddlewaretoken"]')[0].value
  // console.log(period)

  // let data = {
  //             "device": device,
  //             "period": period
  //             }; // add lives_in select value to post data

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
    html: '<strong>COMPUTING SCORES</strong>.', 
    allowOutsideClick: false
  });
  Swal.showLoading();
  
  $.post(host + endpoint)
        .then(resp => {
          resp = JSON.parse(resp)
          
          Swal.getContent().querySelector('strong')
            .textContent = `LOADED READINGS, RENDERING VALUES.`
          console.log(resp);
          return resp;
        })
        .then(resp=> {

            let device = $("#device")[0].value;
            let device_data = resp.data.base_line.filter((e)=>{
                                  return e.device_id == device;
                                })

            draw_baseline(device_data[0]);
            draw_cap_factor_gen1(device_data[0]);
            draw_cap_factor_gen2(device_data[0]);
            draw_felf(device_data[0]);
            draw_cap_fuel_consumption_gen1(device_data[0]);
            draw_cap_fuel_consumption_gen2(device_data[0]);
            draw_emmisions(device_data[0]);
            call_modal(device_data[0]);



            $('#device').on('change', async e => {

              let device = $("#device")[0].value;
              baseline_chart.destroy();

              let device_data = resp.data.base_line.filter((e)=>{
                return e.device_id == device;
              })

              draw_baseline(device_data[0]);
              draw_cap_factor_gen1(device_data[0]);
              draw_cap_factor_gen2(device_data[0]);
              draw_felf(device_data[0]);
              draw_cap_fuel_consumption_gen1(device_data[0]);
              draw_cap_fuel_consumption_gen2(device_data[0]);
              draw_emmisions(device_data[0]);
              call_modal(device_data[0]);
          });

        })
        .then(resp=> {
          Swal.close()
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
          Swal.close()
        }) // post data
}


const draw_baseline = ((device_data)=>{

  // populate_baseline_chart(device_data);

  let forcast_percent = document.getElementById("forcast_percent")
  let forcast_value = document.getElementById("forcast_value")
  let days_gone = document.getElementById("days_gone")
  let forcast_used = document.getElementById("forcast_used")
  let Savings = document.getElementById("savings")
  
  let used = Math.round(device_data.baseline.kwh_usage_so_far)
  let forcast = Math.round(device_data.baseline.forcasted_kwh_usage)
  let days_gone_value = Math.round(device_data.baseline.number_of_days_so_far)
  let percentage = forcast == 0 ? 0 : (used /forcast) * 100;

  let inbound_savings = Math.round(forcast - ((used/days_gone_value)*30));

  

  forcast_value.innerHTML = forcast;
  forcast_used.innerHTML = used;
  days_gone.innerHTML = days_gone_value;
  Savings.innerHTML = inbound_savings;
  Savings.style.color = inbound_savings >= 0 ? "green" : "red";

  
  forcast_percent.innerHTML = ` ${Math.round(percentage)}%<br>Used`
  
      var data = {
        labels: ["So Far", "Forecast remainder"],
        datasets: [
          {
            data: [used, forcast - used],
            backgroundColor: ["#164e44", "#f2f4f8"],
            hoverBackgroundColor: ["#164e44", "#f2f4f8"]
          }
        ]
      };
      
      baseline_chart = new Chart(document.getElementById("baseline-donut"), {
        type: "doughnut",
        data: data,
        options: {
          cutoutPercentage : 80,
          responsive: true,
          legend: {
            display: false
          },
          //* removes automatic chart.js border
          elements: {
            arc: {
              borderWidth: 0
            }
          }
        }
      });

    })


const draw_cap_factor_gen1 = ((device_data)=>{

  let remark1 = document.getElementById("remark1")
  let load_factor1 = document.getElementById("load_factor1")
  let gen1_size = document.getElementsByClassName("gen1_size")
  
  let load_factor1_value = Math.round(device_data.capacity_factor.capacity_factor_gen_1 * 100, 2)
  let gen1_size_value = device_data.capacity_factor.gen1_capacity;

  load_factor1.innerHTML = load_factor1_value;
  gen1_size[0].innerHTML = `${gen1_size_value}KVA`
  gen1_size[1].innerHTML = `${gen1_size_value}KVA`
  remark1.innerHTML = device_data.capacity_factor.verdict_gen_1;
  remark1.style.color = load_factor1_value <=  60 ? "green" : "red";

    
        var data = {
          labels: ["So Far", "Forecast"],
          datasets: [
            {
              data: [load_factor1_value, 100-load_factor1_value],
              backgroundColor: ["#164e44", "#f2f4f8"],
              hoverBackgroundColor: ["#164e44", "#f2f4f8"]
            }
          ]
        };
        
        var cap_factor_chart = new Chart(document.getElementById("capacity-donut1"), {
          type: "doughnut",
          data: data,
          options: {
            cutoutPercentage : 80,
            responsive: true,
            legend: {
              display: false
            },
            //* removes automatic chart.js border
            elements: {
              arc: {
                borderWidth: 0
              }
            },
        
            tooltips: {enabled: false},
          }
        });
  

    })


const draw_cap_fuel_consumption_gen1 = ((device_data)=>{

  let fuel = document.getElementById("fuel1")
  let hours = document.getElementById("hours1")
  
  let fuel_value = device_data.fuel_consumption.gen_1;
  let hours_value = device_data.fuel_consumption.gen_1_hrs;

  fuel.innerHTML = fuel_value;
  hours.innerHTML = hours_value;

    
        var data = {
          labels: ["So Far", "Forecast"],
          datasets: [
            {
              data: [100, 0],
              backgroundColor: ["#164e44", "#f2f4f8"],
              hoverBackgroundColor: ["#164e44", "#f2f4f8"]
            }
          ]
        };
        
        var cap_factor_chart = new Chart(document.getElementById("fuel-donut1"), {
          type: "doughnut",
          data: data,
          options: {
            // cutoutPercentage : 80,
            responsive: true,
            legend: {
              display: false
            },
            //* removes automatic chart.js border
            elements: {
              arc: {
                borderWidth: 0
              }
            },
        
            tooltips: {enabled: false},
          }
        });
  

    })


const draw_cap_fuel_consumption_gen2 = ((device_data)=>{

  let fuel = document.getElementById("fuel2")
  let hours = document.getElementById("hours2")
  
  let fuel_value = device_data.fuel_consumption.gen_2;
  let hours_value = device_data.fuel_consumption.gen_2_hrs;

  fuel.innerHTML = fuel_value;
  hours.innerHTML = hours_value;

    
        var data = {
          labels: ["So Far", "Forecast"],
          datasets: [
            {
              data: [100, 0],
              backgroundColor: ["#164e44", "#f2f4f8"],
              hoverBackgroundColor: ["#164e44", "#f2f4f8"]
            }
          ]
        };
        
        var cap_factor_chart = new Chart(document.getElementById("fuel-donut2"), {
          type: "doughnut",
          data: data,
          options: {
            // cutoutPercentage : 80,
            responsive: true,
            legend: {
              display: false
            },
            //* removes automatic chart.js border
            elements: {
              arc: {
                borderWidth: 0
              }
            },
        
            tooltips: {enabled: false},
          }
        });
  

    })


const draw_cap_factor_gen2 = ((device_data)=>{

  let remark2 = document.getElementById("remark2")
  let load_factor2 = document.getElementById("load_factor2")
  let gen2_size = document.getElementsByClassName("gen2_size")
  
  let load_factor2_value = Math.round(device_data.capacity_factor.capacity_factor_gen_2 * 100, 2)
  let gen2_size_value = device_data.capacity_factor.gen2_capacity;

  load_factor2.innerHTML = load_factor2_value;
  gen2_size[0].innerHTML = `${gen2_size_value}KVA`
  gen2_size[1].innerHTML = `${gen2_size_value}KVA`
  remark2.innerHTML = device_data.capacity_factor.verdict_gen_2;
  remark2.style.color = load_factor2_value <=  60 ? "green" : "red";

    
        var data = {
          labels: ["So Far", "Forecast"],
          datasets: [
            {
              data: [load_factor2_value, 100-load_factor2_value],
              backgroundColor: ["#164e44", "#f2f4f8"],
              hoverBackgroundColor: ["#164e44", "#f2f4f8"]
            }
          ]
        };
        
        var cap_factor_chart = new Chart(document.getElementById("capacity-donut2"), {
          type: "doughnut",
          data: data,
          options: {
            cutoutPercentage : 80,
            responsive: true,
            legend: {
              display: false
            },
            //* removes automatic chart.js border
            elements: {
              arc: {
                borderWidth: 0
              }
            },
        
            tooltips: {enabled: false},
          }
        });
  

    })


const draw_felf = ((device_data)=>{

      let avg_load = document.getElementById("avg_load")
      let peak_load = document.getElementById("peak_load")
      let felf = document.getElementById("felf")
      let felf_remark = document.getElementById("felf_remark")
      
      let load_factor_value = device_data.facility_energy_load_factor.factor_total.toFixed(2)
      let max_load_total = Math.round(device_data.facility_energy_load_factor.max_load_total, 2)
      let avg_load_total = Math.round(device_data.facility_energy_load_factor.avg_load_total, 2)

      avg_load.innerHTML = `Avg load : ${avg_load_total}kW`;
      peak_load.innerHTML = `Peak load : ${max_load_total}kW`;
      felf.innerHTML = load_factor_value;
      felf_remark.innerHTML = device_data.facility_energy_load_factor.remark;

      let green = Math.round(255 * load_factor_value);
      let red = Math.round(255 - green);

      var data = {
        labels: ["So Far", "Forecast"],
        datasets: [
          {
            data: [10, 0],
            backgroundColor: [`rgb(${red},${green},0)`, `rgb(${red},${green},0)`],
            hoverBackgroundColor: ["#af5124", "#f2f4f8"]
          }
        ]
      };
      
      var felf_chart = new Chart(document.getElementById("felf-donut"), {
        type: "doughnut",
        data: data,
        options: {
          // cutoutPercentage : 80,
          animation: false,
          responsive: true,
          legend: {
            display: false
          },
          //* removes automatic chart.js border
          elements: {
            arc: {
              borderWidth: 0
            }
          },
      
          tooltips: { enabled: false }
        }
      });
  

    });

  
const draw_emmisions = ((device_data)=>{

  let prev_grid_emmision = 0;
  let prev_gen1_emmision = 0;
  let prev_gen2_emmision = 0;
  
  let emissions_grid = document.getElementById("emissions-grid")
  let emissions_gens = document.getElementById("emissions-gens")
  let emissions_total = document.getElementById("total_emmisions")
  let emissions_savings = document.getElementById("emissions-savings")

  let grid_kwh = device_data.total_kwh.utility
  let gen1_litres = device_data.fuel_consumption.gen_1
  let gen2_litres = device_data.fuel_consumption.gen_2

  let grid_factor = 0.559 //kgCO2 per kWh  
  let gen_factor  = 2.68 //kgCO2 per liter

  if(device_data.previous_scores.length){

    prev_grid_emmision = (device_data.previous_scores[0].utility_kwh * grid_factor)/1000;
    prev_gen1_emmision = (device_data.previous_scores[0].fuel_consumption_gen1 * gen_factor)/1000;
    prev_gen2_emmision = (device_data.previous_scores[0].fuel_consumption_gen2 * gen_factor)/1000;

  }
  console.log(prev_grid_emmision, prev_gen1_emmision, prev_gen2_emmision)

  let grid_emmisions  = ((grid_kwh * grid_factor)/1000);
  let gen1_emmisions = ((gen1_litres * gen_factor)/1000);
  let gen2_emmisions = ((gen2_litres * gen_factor)/1000);

  console.log(grid_emmisions, gen1_emmisions, gen2_emmisions)

  let previous_total_emmisions = prev_grid_emmision + prev_gen1_emmision + prev_gen2_emmision;
  let emmision_difference = (previous_total_emmisions - (grid_emmisions + gen1_emmisions + gen2_emmisions)).toFixed(0);

  emissions_grid.innerHTML = grid_emmisions.toFixed(2);
  emissions_gens.innerHTML = (gen1_emmisions + gen2_emmisions).toFixed(2);
  emissions_total.innerHTML= `${(grid_emmisions + gen1_emmisions + gen2_emmisions).toFixed(2)}<br>M-Tons`;

  let carbon_per_tree = 3.67
  let saved_or_extra = emmision_difference < 1 ? "more" : "less";
  let number_of_trees = emmision_difference * carbon_per_tree;
  let text_color = emmision_difference <= 0 ? "red" : "green";

  emissions_savings.innerHTML = `${Math.abs(emmision_difference)} tons ${saved_or_extra} emitted this month. <br> (Eqivalent to ${Math.abs(number_of_trees.toFixed(0))} large trees)`;
  emissions_savings.style.color = `${text_color}`;

  

  var data = {
    labels: ["Grid Emmisions", "Gen1 Emmisions", "Gen2 Emmisions"],
    datasets: [
      {
        data: [grid_emmisions.toFixed(2), gen1_emmisions.toFixed(2), gen2_emmisions.toFixed(2)],
        backgroundColor: [`#164e44`, `#008ea5`, `#80315a`],
        // hoverBackgroundColor: ["#af5124", "#af5124", "af5124"]
      }
    ]
  };
  
  var emmisions_chart = new Chart(document.getElementById("carbon-donut"), {
    type: "doughnut",
    data: data,
    options: {
      cutoutPercentage : 80,
      animation: false,
      responsive: true,
      legend: {
        display: false
      },
      //* removes automatic chart.js border
      elements: {
        arc: {
          borderWidth: 2
        }
      },
  
      tooltips: { enabled: true }
    }
  });


})




var populate_baseline_chart = ((device_data)=>{

  let table_container = document.getElementById("table_container");
  let table_text = "";
  let previous_month = device_data.previous_scores.length > 1 ? device_data.previous_scores[1].energy_used : 0;
  table_container.innerHTML = "";

  device_data.previous_scores.forEach(element => {
    let savings = element.baseline_energy - element.energy_used;
    let color = savings >= 0 ? "green" : "red";
    let against_previous = element.energy_used -  previous_month;


    if (device_data.previous_scores.indexOf(element) == device_data.previous_scores.length-1){
      table_text += `
                    <tr class="data-row1">
                    <td>${months[element.month-1]} ${element.year}</td>
                    <td>${(element.baseline_energy).toFixed(0)} </td>
                    <td>${(element.energy_used).toFixed(0)} </td>
                    <td style = "color: ${color};" >${savings.toFixed(0)} </td>
                    <td class="unicode-dash"> &#9473 </td>
                    </tr>
                  `
    } else{
      table_text += `
                    <tr class="data-row1">
                    <td>${months[element.month-1]} ${element.year}</td>
                    <td>${(element.baseline_energy).toFixed(0)} </td>
                    <td>${(element.energy_used).toFixed(0)} </td>
                    <td style = "color: ${color};" >${savings.toFixed(0)} </td>
                    <td> ${against_previous > 0 ? `<img class="arrowUp" src="${host}static/images/uparrow.svg" alt="arrow pointing up">` : `<img class="arrowDown" src="${host}static/images/downarrow.svg" alt="arrow pointing down">`} </td>
                    </tr>
                  `
    }
    previous_month = element.energy_used;
  });

  let template = `<table class="modal-table">
                    <tr class="title-row">
                      <th colspan="5">Baseline-Usage History</th>
                    </tr>
                    <tr class="heading-row">
                      <th>Month</th>
                      <th>Baseline (kWh)</th>
                      <th>Used (kWh)</th>
                      <th>Savings (kWh)</th>
                      <th>Previous </th>
                    </tr>
                    ${table_text}
                    
                </table>
              `;

  table_container.insertAdjacentHTML("afterbegin", template)

});


var populate_fuel_chart = ((device_data)=>{

  let table_container = document.getElementById("table_container");
  let table_text = "";
  table_container.innerHTML = "";

  device_data.previous_scores.forEach(element => {


      table_text += `
                    <tr class="data-row1">
                    <td>${months[element.month-1]} ${element.year}</td>
                    <td>${element.fuel_consumption_gen1} </td>
                    <td>${element.hours_gen1} </td>
                    <td>${element.fuel_consumption_gen2} </td>
                    <td>${element.hours_gen2} </td>
                    </tr>
                  `
  });

  let template = `<table class="modal-table">
                    <tr class="title-row">
                      <th colspan="5">Estimated Fuel History</th>
                    </tr>
                    <tr class="heading-row">
                      <th>Month</th>
                      <th>Fuel <br> (G-1)</th>
                      <th>Hours <br> (G-1)</th>
                      <th>Fuel <br> (G-2)</th>
                      <th>Hours <br> (G-2)</th>
                    </tr>
                    ${table_text}
                    
                </table>
                `

  table_container.insertAdjacentHTML("afterbegin", template)

});

var populate_carbon_chart = ((device_data)=>{

  let table_container = document.getElementById("table_container");
  let table_text = "";
  table_container.innerHTML = "";

  let grid_factor = 0.559 //kgCO2 per kWh  
  let gen_factor  = 2.68 //kgCO2 per liter
 

  device_data.previous_scores.forEach(element => {
      let utility = (element.utility_kwh * grid_factor)/1000
      let gen1    = (element.fuel_consumption_gen1 * gen_factor)/1000
      let gen2    = (element.fuel_consumption_gen2 * gen_factor)/1000
      let total   = utility + gen1 + gen2
      alert(element.utility_kwh)

      table_text += `
                    <tr class="data-row1">
                    <td>${months[element.month-1]} ${element.year}</td>
                    <td>${utility.toFixed(0)} </td>
                    <td>${gen1.toFixed(0)} </td>
                    <td>${gen2.toFixed(0)} </td>
                    <td>${total.toFixed(0)} </td>
                    </tr>
                  `
  });

  let template = `<table class="modal-table">
                    <tr class="title-row">
                      <th colspan="5">Estimated Carbon History</th>
                    </tr>
                    <tr class="heading-row">
                      <th>Month</th>
                      <th>Utility <br> </th>
                      <th>Gen-1 <br> </th>
                      <th>Gen-2 <br> </th>
                      <th>Total <br> </th>
                    </tr>
                    ${table_text}
                    
                </table>
                `

  table_container.insertAdjacentHTML("afterbegin", template)

});


var call_modal = ((device_data)=>{

  for (i = 0; i < historyButtons.length; i++) {
    historyButtons[i].onclick = function(e) {
    historyModal.style.display = "block";
    cardsContainer.classList.add("outside-modal");
    sidebarSection.classList.add("outside-modal");
    sidebarHeader.classList.add("outside-modal");
    contentHeader.classList.add("outside-modal");
    contentSubheader.classList.add("outside-modal");
    panelSection.classList.add("outside-modal");
    otherModals.classList.add("outside-modal");
    
    if (e.target.id == "fuel"){
      populate_fuel_chart(device_data);
    }else if(e.target.id == "baseline"){
      populate_baseline_chart(device_data);
    }else if(e.target.id == "carbon"){
      populate_carbon_chart(device_data);
    };
  };
}
})

var months = [
  'Jan.', 'Feb.', 'Mar.', 'Apr.', 'May.',
  'Jun.', 'Jul.', 'Aug.', 'Sept.',
  'Oct.', 'Nov.', 'Dec.'
  ];

document.addEventListener("click", function(event) {
  let isClickInside = historyModal.contains(event.target);
  let historyClickedOrNot = event.target.className.includes("history-button");

  if (!isClickInside && !historyClickedOrNot) {
    historyModal.style.display = "none";
    cardsContainer.classList.remove("outside-modal");
    sidebarSection.classList.remove("outside-modal");
    sidebarHeader.classList.remove("outside-modal");
    contentHeader.classList.remove("outside-modal");
    contentSubheader.classList.remove("outside-modal");
    panelSection.classList.remove("outside-modal");
    otherModals.classList.remove("outside-modal");
  }
});


