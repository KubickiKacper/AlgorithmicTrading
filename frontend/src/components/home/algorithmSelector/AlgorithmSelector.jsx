import {useState} from "react"
import "./AlgorithmSelector.css"
import ProfitDisplay from "./ProfitDisplay"

function AlgorithmSelector({onSubmit, profitData}) {
  const [algorithm, setAlgorithm] = useState("moving_average")
  const [firstDayBuy, setFirstDayBuy] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit({algorithm, first_day_buy: firstDayBuy})
  }

  return (
    <form className="algorithm-selector" onSubmit={handleSubmit}>
      <ProfitDisplay profitData={profitData}/>
      <label className="algorithm-selector-label">
        Algorithm:
        <select value={algorithm} onChange={(e) => setAlgorithm(e.target.value)}>
          <option value="none">None</option>
          <option value="MAC">Moving Average</option>
          <option value="buy_and_hold">Buy and Hold</option>
          <option value="rsi_based">RSI-Based</option>
        </select>
      </label>

      <label className="toggle-label">
        <span className="toggle-text">First Day Buy</span>
        <div className="toggle-switch">
          <input
            type="checkbox"
            checked={firstDayBuy}
            onChange={(e) => setFirstDayBuy(e.target.checked)}
          />
          <span className="slider"></span>
        </div>
      </label>

      <button type="submit">Select Algorithm</button>
    </form>
  )
}

export default AlgorithmSelector