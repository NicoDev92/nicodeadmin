document.addEventListener('DOMContentLoaded', function () {
  var ctx = document.getElementById("myBarChart");

  if (ctx) {
    var barLabels = JSON.parse(ctx.getAttribute('data-productos'));
    var barData = JSON.parse(ctx.getAttribute('data-cantidades'));
    var barColors = generateRandomColors(barLabels.length);

    var myBarChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: barLabels,
        datasets: [{
          label: "Cantidad Vendida",
          backgroundColor: barColors,
          hoverBackgroundColor: barColors,
          borderColor: barColors,
          borderWidth: 1,
          data: barData,
        }],
      },
      options: {
        maintainAspectRatio: false,
        layout: {
          padding: {
            left: 10,
            right: 25,
            top: 25,
            bottom: 0
          }
        },
        scales: {
          xAxes: [{
            ticks: {
              maxRotation: 90,
              minRotation: 0,
              callback: function (value, index, values) {
                if (value.length > 10) {
                  return value.substring(0, 10) + '...';
                }
                return value;
              }
            },
            gridLines: {
              display: false
            }
          }],
          yAxes: [{
            ticks: {
              min: 0,
              maxTicksLimit: 5,
              padding: 10,
              callback: function (value, index, values) {
                return number_format(value);
              }
            },
            gridLines: {
              color: "rgb(234, 236, 244)",
              zeroLineColor: "rgb(234, 236, 244)",
              drawBorder: false,
              borderDash: [2],
              zeroLineBorderDash: [2]
            }
          }],
        },
        legend: {
          display: false
        },
        tooltips: {
          titleMarginBottom: 10,
          titleFontColor: '#6e707e',
          titleFontSize: 14,
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          borderColor: '#dddfeb',
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: false,
          caretPadding: 10,
          callbacks: {
            label: function (tooltipItem, chart) {
              var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
              return datasetLabel + ': ' + number_format(tooltipItem.yLabel);
            }
          }
        },
      }
    });
  }
});

// Función para generar colores aleatorios en formato hexadecimal
function generateRandomColors(numColors) {
  var colors = [];
  for (var i = 0; i < numColors; i++) {
    var color = '#' + Math.floor(Math.random() * 16777215).toString(16);
    colors.push(color);
  }
  return colors;
}
