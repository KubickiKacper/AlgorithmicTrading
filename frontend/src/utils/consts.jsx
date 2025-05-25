export const apiUrl = 'http://localhost:5000/'

export const LINE_COLORS = {
  "SHORT MA": '#3399ff',
  "LONG MA": '#00e396',
  "RSI": '#FF9900',
  "MIDDLE_BAND": '#cccccc',
  "UPPER_BAND": '#FF4560',
  "LOWER_BAND": '#00E396',
  "DEFAULT": '#3399ff',
}

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
  xaxis: {
    type: "datetime",
    labels: {style: {colors: "#ccc"}}
  },
  yaxis: {
    tooltip: {enabled: true},
    labels: {
      style: {colors: "#ccc"},
      formatter: (value) => value.toFixed(2),
    },
  },
  grid: {
    borderColor: "#444"
  },
}

export const RSI_CHART_OPTIONS = {
  ...CHART_OPTIONS,
  chart: {
    ...CHART_OPTIONS.chart,
    id: "rsi-chart",
    group: "market-charts", // Synchronizacja z wykresem świecowym
    height: 200,
    zoom: {
      enabled: true,
    },
  },
  title: {
    text: "RSI",
    align: "left",
    labels: {style: {colors: "#ccc"}}
  },
  xaxis: {
    type: "datetime",
    title: {
      text: "Data",
      style: {
        color: "#ccc",
      },
    },
    labels: {
      style: {
        colors: "#ccc",
      },
    },
  },
  yaxis: {
    min: 0,
    max: 100,
    tickAmount: 5,
    title: {
      text: "Wartość",
      style: {
        color: "#ccc",
      },
    },
    labels: {
      style: {
        colors: "#ccc",
      },
      formatter: (value) => value.toFixed(0),
    },
  },
  annotations: {
    yaxis: [
      {
        y: 70,
        borderColor: '#FF4560',
        label: {
          borderColor: '#FF4560',
          style: {
            color: '#fff',
            background: '#FF4560',
          },
          text: 'Overbought (70)',
        },
      },
      {
        y: 30,
        borderColor: '#00E396',
        label: {
          borderColor: '#00E396',
          style: {
            color: '#fff',
            background: '#00E396',
          },
          text: 'Oversold (30)',
        },
      },
    ],
  },
  stroke: {
    curve: 'smooth',
    width: 2,
  },
  colors: [LINE_COLORS.RSI],
}