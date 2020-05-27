/* Activity Chart */

var chartactivity = document.getElementById('ActivityChart').getContext("2d");

var gradientStroke = chartactivity.createLinearGradient(200, 0, 100, 0);
gradientStroke.addColorStop(0, "rgba(124, 39, 235, 1)");
gradientStroke.addColorStop(1, "rgba(124, 39, 235, 1)");

var gradientStroke2 = chartactivity.createLinearGradient(200, 0, 100, 0);
gradientStroke2.addColorStop(0, "rgba(255, 99, 180, 1)");
gradientStroke2.addColorStop(1, "rgba(255, 99, 180, 1)");

var gradientStroke3 = chartactivity.createLinearGradient(200, 0, 100, 0);
gradientStroke3.addColorStop(0, "rgba(0, 220, 255, 1)");
gradientStroke3.addColorStop(1, "rgba(0, 220, 255, 1)");


var gradientFill = chartactivity.createLinearGradient(50, 150, 0, 350);
gradientFill.addColorStop(0, "rgba(100, 204, 63, 0.5)");
gradientFill.addColorStop(1, "rgba(100, 204, 63, 0)");

var gradientFill2 = chartactivity.createLinearGradient(0, 0, 0, 350);
gradientFill2.addColorStop(0, "rgba(255, 91, 204, 0.5)");
gradientFill2.addColorStop(1, "rgba(255, 91, 204, 0)");

var gradientFill3 = chartactivity.createLinearGradient(0, 0, 0, 350);
gradientFill3.addColorStop(0, "rgba(128, 182, 244, 0.5)");
gradientFill3.addColorStop(1, "rgba(128, 182, 244, 0)");



var ActivityChart = new Chart(chartactivity, {
    type: 'bar',
    yAxisID: "kW-Hours",
    xAxisID: "Days",
    data: {
        labels: [50,50,50,50,50,50,50,50,50,50],
        datasets: [
            {
            label: "Mains (KWh)",
            borderColor: gradientStroke,
            pointBorderColor: gradientStroke,
            pointBackgroundColor: "rgba(255, 255, 255, 1)",
            pointHoverBackgroundColor: "rgba(128, 182, 244, 1)",
            pointHoverBorderColor: gradientStroke,
            pointBorderWidth: 1,
            pointHoverRadius: 3,
            pointHoverBorderWidth: 1,
            pointRadius: 3,
            fill: true,
			backgroundColor: gradientStroke,
            borderWidth: 2,
            data: [50,50,50,50,50,50,50,50,50,50]
            },	
            {
            label: "Gen 1 (KWh)",
            borderColor: gradientStroke2,
            pointBorderColor: gradientStroke2,
            pointBackgroundColor: "rgba(255, 255, 255, 1)",
            pointHoverBackgroundColor: "rgba(128, 182, 244, 1)",
            pointHoverBorderColor: gradientStroke2,
            pointBorderWidth: 1,
            pointHoverRadius: 3,
            pointHoverBorderWidth: 1,
            pointRadius: 3,
            fill: true,
			backgroundColor: gradientStroke2,
            borderWidth: 2,
            data: [50,50,50,50,50,50,50,50,50,50]
            },
            {
            label: "Gen 2 (KWh)",
            borderColor: gradientStroke3,
            pointBorderColor: gradientStroke3,
            pointBackgroundColor: "rgba(255, 255, 255, 1)",
            pointHoverBackgroundColor: "rgba(128, 182, 244, 1)",
            pointHoverBorderColor: gradientStroke3,
            pointBorderWidth: 1,
            pointHoverRadius: 3,
            pointHoverBorderWidth: 1,
            pointRadius: 3,
            fill: true,
			backgroundColor: gradientStroke3,
            borderWidth: 2,
            data: [50,50,50,50,50,50,50,50,50,50]
        }
		]
    },
    options: {          
        legend: {
            position: "top",
            labels: {
                boxWidth: 15,
				padding: 15
            },
            title: {
                display: true,
                text: 'Daily usage so far this month(kW-Hours)'
            }
        },
        scales: {
            yAxes: [{
                ticks: {
                    fontColor: "rgba(0,0,0,0.5)",
                    fontStyle: "bold",
                    beginAtZero: true,
                    maxTicksLimit: 5,
                    padding: 20
                },
                gridLines: {
                    drawTicks: false,
                    display: false
                },
                scaleLabel : {
                    display: true,
                    labelString: "Kilowatt-Hour values"
                },
                stacked: true // this also..

            }],
            xAxes: [{
                gridLines: {
                    zeroLineColor: "transparent"
                },
                ticks: {
                    padding: 20,
                    fontColor: "rgba(0,0,0,0.5)",
                    fontStyle: "bold"
                },
                scaleLabel : {
                    display: true,
                    labelString: "Days of the month"
                },
                stacked: true // this should be set to make the bars stacked
            }]
        },
        tooltips: {
            mode: "index"
        }
    }
});
console.dir(ActivityChart.data);

/* Diseases Chart */

var chartdiseases = document.getElementById('DiseasesChart').getContext("2d");

var DiseasesChart = new Chart(chartdiseases, {
    type: 'doughnut',
    data: {
        labels: ["GEN-1", "GEN-2", "PHCN"],
        datasets: [{
            label: "Data",
            fill: true,
			backgroundColor: [
            "rgba(255, 99, 180, 1)",
            "rgba(0, 220, 255, 1)",
            "rgba(124, 39, 235, 1)"
			],
            borderWidth: 2,
            data: [1, 1, 1]
        }]
    },
    options: {    
        title: {
            display: true,
            text: 'Usage so far this month(Hrs.)'
        },      
        legend: {
            position: "bottom",
            labels: {
                boxWidth: 15,
				padding: 15
            },
            tooltips: {
                mode: "index"
            }
			
        }
    }
});

/* Reports Chart */

var chartreports = document.getElementById('ReportsChart').getContext("2d");

var ReportsChart = new Chart(chartreports, {
    type: 'line',
    data: {
        labels: ["SU", "MO", "TU", "WE", "TH", "FR", "SA"],
        datasets: [{
            label: "Reports",
            borderColor: "#5616f5",
            pointBorderColor: "#5616f5",
            pointBackgroundColor: "rgba(255, 255, 255, 1)",
            pointHoverBackgroundColor: "rgba(128, 182, 244, 1)",
            pointHoverBorderColor: gradientStroke,
            pointBorderWidth: 1,
            pointHoverRadius: 3,
            pointHoverBorderWidth: 1,
            pointRadius: 2,
            fill: true,
			backgroundColor: gradientFill,
            borderWidth: 1,
            data: [1, 10, 2, 5, 1, 7, 0]
        }
		]
    },
    options: {          
        legend: {
            position: "top",
            labels: {
                boxWidth: 15,
				padding: 5
            }
        },
        scales: {
            yAxes: [{
                ticks: {
                    display: false
                },
                gridLines: {
                    drawTicks: false,
                    display: false,
					drawBorder: false
                }

            }],
            xAxes: [{
                gridLines: {
                    zeroLineColor: "transparent",
					display: false,
					drawBorder: false
                },
                ticks: {
                    padding: 0,
                    fontColor: "rgba(0,0,0,0.2)",
                    fontStyle: "bold"
                }
            }]
        }
    }
});


/* Custom Chart */

var chartcustom = document.getElementById('CustomChart').getContext("2d");

var CustomChart = new Chart(chartcustom, {
    type: 'bar',
    data: {
        labels: ["SU", "MO", "TU", "WE", "TH", "FR", "SA"],
        datasets: [{
            label: "Reports",
            pointBorderColor: "#5616f5",
            pointBackgroundColor: "rgba(255, 255, 255, 1)",
            pointHoverBackgroundColor: "rgba(128, 182, 244, 1)",
            pointHoverBorderColor: gradientStroke,
            pointBorderWidth: 2,
            pointHoverRadius: 6,
            pointHoverBorderWidth: 2,
            pointRadius: 6,
            fill: false,
			showLine: false,
            borderWidth: 2,
            data: [21, 12, 20, 16, 11, 25, 18]
        }
		]
    },
    options: {          
        legend: {
            position: "top",
            labels: {
                boxWidth: 15,
				padding: 5
            }
        },
        scales: {
            xAxes: [{
                gridLines: {
                    zeroLineColor: "transparent",
					display: false,
					drawBorder: false
                },
                ticks: {
                    padding: 0,
                    fontColor: "rgba(0,0,0,0.2)",
                    fontStyle: "bold"
                }
            }]
        }
    }
});


// POWER CHARTS LINE BASED CHART

var chartpower = document.getElementById('power_chart').getContext("2d");


var power_chart = new Chart(chartpower, {
    type: 'line',
    yAxisID: "k-Watts",
    xAxisID: "Location",
    data: {
        labels: ["IKOYI", "MAIN", "HQTRS", "MRYLND", "OGBA", "IKJ", "V.I"],
        datasets: [{
            label: "Max kW",
            borderColor: gradientStroke,
            pointBorderColor: gradientStroke,
            pointBackgroundColor: "rgba(255, 255, 255, 1)",
            pointHoverBackgroundColor: "rgba(128, 182, 244, 1)",
            pointHoverBorderColor: gradientStroke,
            pointBorderWidth: 1,
            pointHoverRadius: 3,
            pointHoverBorderWidth: 1,
            pointRadius: 3,
            fill: true,
			backgroundColor: gradientFill,
            borderWidth: 2,
            data: [40, 4, 31, 10, 34, 12, 48]
        },	{
            label: "Min kW",
            borderColor: gradientStroke2,
            pointBorderColor: gradientStroke2,
            pointBackgroundColor: "rgba(255, 255, 255, 1)",
            pointHoverBackgroundColor: "rgba(128, 182, 244, 1)",
            pointHoverBorderColor: gradientStroke2,
            pointBorderWidth: 1,
            pointHoverRadius: 3,
            pointHoverBorderWidth: 1,
            pointRadius: 3,
            fill: true,
			backgroundColor: gradientFill2,
            borderWidth: 2,
            data: [26, 12, 20, 16, 6, 25, 18]
        }
		]
    },
    options: {          
        legend: {
            position: "top",
            labels: {
                boxWidth: 15,
				padding: 15
            },
            title: {
                display: true,
                text: 'Usage so far this month(kWatts)'
            }
        },
        scales: {
            yAxes: [{
                ticks: {
                    fontColor: "rgba(0,0,0,0.5)",
                    fontStyle: "bold",
                    beginAtZero: true,
                    maxTicksLimit: 5,
                    padding: 20
                },
                gridLines: {
                    drawTicks: false,
                    display: false
                }

            }],
            xAxes: [{
                gridLines: {
                    zeroLineColor: "transparent"
                },
                ticks: {
                    padding: 20,
                    fontColor: "rgba(0,0,0,0.5)",
                    fontStyle: "bold"
                }
            }]
        }
    }
});