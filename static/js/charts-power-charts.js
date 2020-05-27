/* Activity Chart */

var chartactivity = document.getElementById('ActivityChart').getContext("2d");

var gradientStroke = chartactivity.createLinearGradient(200, 0, 100, 0);
gradientStroke.addColorStop(0, "rgba(58, 233, 245, 1)");
gradientStroke.addColorStop(1, "rgba(18, 216, 227, 1)");

var gradientStroke2 = chartactivity.createLinearGradient(200, 0, 100, 0);
gradientStroke2.addColorStop(0, "rgba(255, 92, 203, 1)");
gradientStroke2.addColorStop(1, "rgba(253, 133, 168, 1)");    

var gradientStroke3 = chartactivity.createLinearGradient(200, 0, 100, 0);
gradientStroke3.addColorStop(0, "rgba(255, 200, 60, 1)");
gradientStroke3.addColorStop(1, "rgba(253, 255, 50, 1)");    

var gradientFill = chartactivity.createLinearGradient(0, 0, 0, 350);
gradientFill.addColorStop(0, "rgba(128, 182, 244, 0.5)");
gradientFill.addColorStop(1, "rgba(128, 182, 244, 0)");

var gradientFill2 = chartactivity.createLinearGradient(0, 0, 0, 350);
gradientFill2.addColorStop(0, "rgba(255, 91, 204, 0.5)");
gradientFill2.addColorStop(1, "rgba(255, 91, 204, 0)");

var gradientFill3 = chartactivity.createLinearGradient(200, 100, 0, 350);
gradientFill3.addColorStop(0, "rgba(255, 204, 63, 0.5)");
gradientFill3.addColorStop(1, "rgba(255, 204, 63, 0)");

var ActivityChart = new Chart(chartactivity, {
    type: 'line',
    yAxisID: "k-Watts",
    xAxisID: "Location",
    data: {
        labels: ["1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm"],
        datasets: [{
            label: "L1 kW",
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
            label: "L2 kW",
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
        },
        	{
            label: "L3 kW",
            borderColor: gradientStroke3,
            pointBorderColor: gradientStroke3,
            pointBackgroundColor: "rgba(255, 255, 255, 1)",
            pointHoverBackgroundColor: "rgba(128, 182, 244, 1)",
            pointHoverBorderColor: gradientStroke2,
            pointBorderWidth: 1,
            pointHoverRadius: 3,
            pointHoverBorderWidth: 1,
            pointRadius: 3,
            fill: true,
			backgroundColor: gradientFill3,
            borderWidth: 2,
            data: [30, 22, 50, 26, 6, 20, 38]
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

