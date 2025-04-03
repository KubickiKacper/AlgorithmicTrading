import {useState} from "react"
import "./StockSelector.css"

function StockSelector({onSubmit}) {
  const [ticker, setTicker] = useState("BTC-USD")
  const [interval, setInterval] = useState("1wk")
  const [startDate, setStartDate] = useState("2019-02-01")
  const [endDate, setEndDate] = useState("2025-03-02")

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit({ticker, interval, start_date: startDate, end_date: endDate})
  }

  return (
    <form className="stock-selector" onSubmit={handleSubmit}>
      <label>
        Stock:
        <select value={ticker} onChange={(e) => setTicker(e.target.value)}>
          <option value="BTC-USD">Bitcoin (BTC-USD)</option>
          <option value="AAPL">Apple (AAPL)</option>
          <option value="TSLA">Tesla (TSLA)</option>
          <option value="GOOGL">Google (GOOGL)</option>
        </select>
      </label>

      <label>
        Interval:
        <select value={interval} onChange={(e) => setInterval(e.target.value)}>
          <option value="1d">1 day</option>
          <option value="1wk">1 week</option>
          <option value="1mo">1 month</option>
        </select>
      </label>

      <label>
        Start date:
        <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)}/>
      </label>
      <label>
        End date:
        <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)}/>
      </label>

      <button type="submit">Load data</button>
    </form>
  )
}

export default StockSelector
