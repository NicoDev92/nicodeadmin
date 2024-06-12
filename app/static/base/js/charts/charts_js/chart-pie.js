// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Función para generar colores aleatorios
function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

document.addEventListener('DOMContentLoaded', function () {
  var ctx = document.getElementById("myPieChart");

  var labels = JSON.parse(ctx.getAttribute('data-labels'));
  var data = JSON.parse(ctx.getAttribute('data-data'));



  if (ctx) {
    // Genera una lista de colores en función de la cantidad de etiquetas
    var backgroundColors = [];
    var hoverBackgroundColors = [];
    for (var i = 0; i < labels.length; i++) {
      var color = getRandomColor();
      backgroundColors.push(color);
      hoverBackgroundColors.push(color);
    }

    var myPieChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: backgroundColors,
          hoverBackgroundColor: hoverBackgroundColors,
          hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
      },
      options: {
        maintainAspectRatio: false,
        tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          borderColor: '#dddfeb',
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: false,
          caretPadding: 10,
        },
        legend: {
          display: false
        },
        cutoutPercentage: 80,
      },
    });

    // Calcular la suma total de los gastos y agregarla al pie de la tarjeta
    var totalGastos = 0;
    for (d in data) {
      totalGastos += parseFloat(data[d]);
    }
    var totalGastosText = document.createElement('div');
    totalGastosText.textContent = 'Gastos mensuales totales: $' + totalGastos.toFixed(2);
    totalGastosText.classList.add('font-weight-bold'); // Agregar clase Bootstrap
    totalGastosText.classList.add('text-center'); // Agregar clase Bootstrap
    document.querySelector('.card-body').appendChild(totalGastosText);
  }
});
