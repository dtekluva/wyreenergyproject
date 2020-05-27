/* Activity Chart */

var chartactivity = document.getElementById('ActivityChart').getContext("2d");

var gradientStroke = chartactivity.createLinearGradient(200, 0, 100, 0);
gradientStroke.addColorStop(0, "rgba(58, 233, 245, 1)");
gradientStroke.addColorStop(1, "rgba(58, 233, 245, 1)");

var gradientStroke2 = chartactivity.createLinearGradient(200, 0, 100, 0);
gradientStroke2.addColorStop(0, "rgba(255, 92, 203, 1)");
gradientStroke2.addColorStop(1, "rgba(253, 133, 168, 1)");    

var gradientStroke3 = chartactivity.createLinearGradient(200, 0, 100, 0);
gradientStroke3.addColorStop(0, "rgba(255, 200, 60, 1)");
gradientStroke3.addColorStop(1, "rgba(253, 255, 50, 1)");    

var gradientStroke4 = chartactivity.createLinearGradient(200, 0, 100, 0);
gradientStroke4.addColorStop(0, "rgba(55, 200, 60, 1)");
gradientStroke4.addColorStop(1, "rgba(53, 255, 50, 1)");    

var gradientFill = chartactivity.createLinearGradient(0, 0, 0, 350);
gradientFill.addColorStop(0, "rgba(128, 182, 244, 0.5)");
gradientFill.addColorStop(1, "rgba(128, 182, 244, 0)");

var gradientFill2 = chartactivity.createLinearGradient(0, 0, 0, 350);
gradientFill2.addColorStop(0, "rgba(255, 91, 204, 0.5)");
gradientFill2.addColorStop(1, "rgba(255, 91, 204, 0)");

var gradientFill3 = chartactivity.createLinearGradient(200, 100, 0, 350);
gradientFill3.addColorStop(0, "rgba(255, 204, 63, 0.5)");
gradientFill3.addColorStop(1, "rgba(255, 204, 63, 0)");

var gradientFill4 = chartactivity.createLinearGradient(50, 150, 0, 350);
gradientFill4.addColorStop(0, "rgba(100, 204, 63, 0.5)");
gradientFill4.addColorStop(1, "rgba(100, 204, 63, 0)");

var ActivityChart = new Chart(chartactivity, {
    type: 'line',
    yAxisID: "k-Volts",
    xAxisID: "Location",
    data: {
        labels: ["1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm"],
        datasets: [{
            label: "L1 Volts",
            borderColor: "#55bae7",
            backgroundColor: "#55cae7",
            // pointBackgroundColor: "rgba(255, 255, 255, 1)",
            // pointBorderColor: "#55bae7",
            // pointHoverBackgroundColor: "#55bae7",
            // pointHoverBorderColor: "#55bae7",
            pointRadius: 1,
            fill: false,
			backgroundColor: "#55cae7",
            borderWidth: 1,
            data: []
        },	{
            label: "L2 Volts",
            borderColor: "#C20F0F",
            backgroundColor: "#C20F0F",
            // pointBackgroundColor: "rgba(255, 255, 255, 1)",
            // pointBorderColor: "#C20F0F",
            // pointHoverBackgroundColor: "#C20F0F",
            // pointHoverBorderColor: "#C20F0F",
            pointRadius: 1,
            fill: false,
			backgroundColor: "#C20F0F",
            borderWidth: 1,
            data: []
        },
        	{
            label: "L3 Volts",
            borderColor: "#5E8A00",
            backgroundColor: "#5E8A00",
            // pointBackgroundColor: "rgba(255, 255, 255, 1)",
            // pointBorderColor: "#7DB800",
            // pointHoverBackgroundColor: "#7DB800",
            // pointHoverBorderColor: "#7DB800",
            pointRadius: 1,
            fill: false,
			backgroundColor: "#5E8A00",
            borderWidth: 1,
            data: []
        },
        	{
            label: "Freq Hertz(Avg.)",
            borderColor: "#FFB56B",
            backgroundColor: "#FFB56B",
            // pointBackgroundColor: "rgba(255, 255, 255, 1)",
            // pointBorderColor: "#7DB800",
            // pointHoverBackgroundColor: "#7DB800",
            // pointHoverBorderColor: "#7DB800",
            pointRadius: 1,
            fill: false,
			backgroundColor: "#FFB56B",
            borderWidth: 1,
            data: []
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
                text: 'Usage so far this month(Volts)'
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
        },
        tooltips: {
            mode: 'index'
         }
    }
});