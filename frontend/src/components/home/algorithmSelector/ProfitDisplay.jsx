import "./ProfitDisplay.css"

function ProfitDisplay({profitData}) {
  return (
    <div className="profit-display">
      <div className="profit-item">
        <span className="profit-label">Total Profit:</span>
        <span className="profit-value">{profitData.profit_percentage.toFixed(2)}%</span>
      </div>
      <div className="profit-item">
        <span className="profit-label">Alg. Profit:</span>
        <span className="profit-value">{profitData.algorithm_profit_percentage.toFixed(2)}%</span>
      </div>
    </div>
  )
}

export default ProfitDisplay