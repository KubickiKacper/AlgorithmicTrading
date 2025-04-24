import './Home.css'
import {useState, useCallback} from "react"
import CandlestickChart from "./candlestickChart/CandlestickChart"
import StockSelector from "./stockSelector/StockSelector"
import AlgorithmSelector from "./algorithmSelector/AlgorithmSelector"

function Home() {
  const [requestData, setRequestData] = useState({
    ticker: "BTC-USD",
    start_date: "2019-02-01",
    end_date: "2025-03-02",
    interval: "1wk",
    algorithm: "moving_average",
    first_day_buy: false,
  })

  const [profitData, setProfitData] = useState({
    profit_percentage: 0,
    algorithm_profit_percentage: 0,
  })

  const handleStockSubmit = (stockData) => {
    setRequestData((prev) => ({...prev, ...stockData}))
  }

  const handleAlgorithmSubmit = (algorithmData) => {
    setRequestData((prev) => ({...prev, ...algorithmData}))
  }

  const handleProfitDataUpdate = useCallback((newProfitData) => {
    setProfitData((prev) => {
      if (
        prev.profit_percentage !== newProfitData.profit_percentage ||
        prev.algorithm_profit_percentage !== newProfitData.algorithm_profit_percentage
      ) {
        return newProfitData
      }
      return prev
    })
  }, [])

  return (
    <div className='Home'>
      <AlgorithmSelector onSubmit={handleAlgorithmSubmit} profitData={profitData}/>
      <StockSelector onSubmit={handleStockSubmit}/>
      <CandlestickChart requestData={requestData} onProfitDataUpdate={handleProfitDataUpdate}/>
    </div>
  )
}

export default Home