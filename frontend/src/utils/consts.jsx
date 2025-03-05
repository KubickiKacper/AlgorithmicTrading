export const apiUrl = 'http://localhost:5000/'

export const CHART_OPTIONS = {
  chart: {
    type: "candlestick",
    height: 350,
    animations: {
      enabled: false,
    },
    zoom: {
      enabled: true,
      type: 'x',
      autoScaleYaxis: true,
    }
    },
  annotations: {
    xaxis: [
      {
        borderColor: "#FF4560",
        label: {
          style: {
            color: "#fff",
            background: "#FF4560",
          },
        },
      },
    ],
  },
  xaxis: {
    type: "datetime",
    labels: {style: {colors: "#ccc"}}
  },
  yaxis: {
    tooltip: {enabled: true},
    labels: {style: {colors: "#ccc"}},
  },
  grid: {
    borderColor: "#444"
  }
}