var data = {};
// Configuration options
var options = {
  legend: {
    display: false,
  },
  title: {
    display: true,
    text: "Temperature",
  },
  maintainAspectRatio: false, // This prevents the chart from maintaining a fixed aspect ratio
  responsive: true,
  scales: {
    xAxes: [
      {
        ticks: {
          display: false,
        },
      },
    ],
    yAxes: [
      {
        ticks: {
          display: false,
        },
      },
    ],
  },
};

var soil_label = JSON.parse(
  "{{ data.greenroom.soil_chart_label }}".replace(/&#39;/g, '"')
);
var light_label = JSON.parse(
  "{{ data.greenroom.light_chart_label }}".replace(/&#39;/g, '"')
);
var temp_label = JSON.parse(
  "{{ data.greenroom.temperature_chart_label }}".replace(/&#39;/g, '"')
);

var soil_data = JSON.parse(
  "{{ data.greenroom.soil_chart_data }}".replace(/&#39;/g, '"')
);
var light_data = JSON.parse(
  "{{ data.greenroom.light_chart_data }}".replace(/&#39;/g, '"')
);
var temp_data = JSON.parse(
  "{{ data.greenroom.temperature_chart_data }}".replace(/&#39;/g, '"')
);

chart_1_data = {
  labels: soil_label,
  datasets: [
    {
      data: soil_data,
      borderColor: "rgb(75, 192, 192)",
      borderWidth: 2,
      fill: false, // Set fill to false to show only the line
    },
  ],
};
chart_2_data = {
  labels: light_label,
  datasets: [
    {
      data: light_data,
      borderColor: "rgb(75, 192, 192)",
      borderWidth: 2,
      fill: false, // Set fill to false to show only the line
    },
  ],
};
chart_3_data = {
  labels: temp_label,
  datasets: [
    {
      data: temp_data,
      borderColor: "rgb(75, 192, 192)",
      borderWidth: 2,
      fill: false, // Set fill to false to show only the line
    },
  ],
};

options.title.text = "Soil Moisture";
var chart = new Chart(document.getElementById("lineChart0").getContext("2d"), {
  type: "line",
  data: chart_1_data,
  options: options,
});
options.title.text = "Light";
var chart = new Chart(document.getElementById("lineChart1").getContext("2d"), {
  type: "line",
  data: chart_2_data,
  options: options,
});
options.title.text = "Temperature";
var chart = new Chart(document.getElementById("lineChart2").getContext("2d"), {
  type: "line",
  data: chart_3_data,
  options: options,
});

var data = {};
// Configuration options
var options = {
  legend: {
    display: false,
  },
  title: {
    display: true,
    text: "Temperature",
  },
  maintainAspectRatio: false, // This prevents the chart from maintaining a fixed aspect ratio
  responsive: true,
  scales: {
    xAxes: [
      {
        ticks: {
          display: false,
        },
      },
    ],
    yAxes: [
      {
        ticks: {
          display: false,
        },
      },
    ],
  },
};

var soil_label = JSON.parse(
  "{{ data.greenroom.soil_chart_label }}".replace(/&#39;/g, '"')
);
var light_label = JSON.parse(
  "{{ data.greenroom.light_chart_label }}".replace(/&#39;/g, '"')
);
var temp_label = JSON.parse(
  "{{ data.greenroom.temperature_chart_label }}".replace(/&#39;/g, '"')
);

var soil_data = JSON.parse(
  "{{ data.greenroom.soil_chart_data }}".replace(/&#39;/g, '"')
);
var light_data = JSON.parse(
  "{{ data.greenroom.light_chart_data }}".replace(/&#39;/g, '"')
);
var temp_data = JSON.parse(
  "{{ data.greenroom.temperature_chart_data }}".replace(/&#39;/g, '"')
);

chart_1_data = {
  labels: soil_label,
  datasets: [
    {
      data: soil_data,
      borderColor: "rgb(75, 192, 192)",
      borderWidth: 2,
      fill: false, // Set fill to false to show only the line
    },
  ],
};
chart_2_data = {
  labels: light_label,
  datasets: [
    {
      data: light_data,
      borderColor: "rgb(75, 192, 192)",
      borderWidth: 2,
      fill: false, // Set fill to false to show only the line
    },
  ],
};
chart_3_data = {
  labels: temp_label,
  datasets: [
    {
      data: temp_data,
      borderColor: "rgb(75, 192, 192)",
      borderWidth: 2,
      fill: false, // Set fill to false to show only the line
    },
  ],
};

options.title.text = "Soil Moisture";
var chart = new Chart(document.getElementById("lineChart0").getContext("2d"), {
  type: "line",
  data: chart_1_data,
  options: options,
});
options.title.text = "Light";
var chart = new Chart(document.getElementById("lineChart1").getContext("2d"), {
  type: "line",
  data: chart_2_data,
  options: options,
});
options.title.text = "Temperature";
var chart = new Chart(document.getElementById("lineChart2").getContext("2d"), {
  type: "line",
  data: chart_3_data,
  options: options,
});

window.jsPDF = window.jspdf.jsPDF;
window.html2canvas = html2canvas;

var doc = new jsPDF();
var chart_render_list = [];
var elements = [
  {
    type: "text",
    value: "{{data.greenroom.name}} Report",
    x: 10,
    y: 10,
  },
  { type: "text", value: "Environment Monitoring Data", x: 10, y: 30 },
  {
    type: "text",
    value:
      "Soil Moisture Data for Date Range(20 October 2023 - 20 November 2023)",
    x: 10,
    y: 70,
  },
  { type: "chart", id: "linechart01", x: 10, y: 80 },
  {
    type: "text",
    value:
      "Soil Moisture Data for Date Range(20 October 2023 - 20 November 2023)",
    x: 10,
    y: 120,
  },
  { type: "chart", id: "linechart02", x: 10, y: 130 },
  {
    type: "text",
    value:
      "Soil Moisture Data for Date Range(20 October 2023 - 20 November 2023)",
    x: 10,
    y: 170,
  },
  { type: "chart", id: "linechart03", x: 10, y: 180 },
];

function addChartToPDF(chartElement, x, y) {
  return new Promise((resolve) => {
    html2canvas(chartElement).then(function (canvas) {
      const imgData = canvas.toDataURL("image/png", 1.0);
      doc.addImage(imgData, "PNG", x, y);
      resolve();
    });
  });
}

function renderElement(element) {
  if (element.type == "text") {
    doc.text(element.value, element.x, element.y);
  } else if (element.type == "chart") {
    chart_render_list.push(
      addChartToPDF(document.getElementById(element.id), element.x, element.y)
    );
  }
}

// Capture and add the three charts to the PDF
Promise.all(chart_render_list).then(() => {
  // Save the PDF after all charts have been added
  doc.save("report.pdf");
});
