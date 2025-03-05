import './Home.css'
import {useState} from "react"
import CandlestickChart from "./candlestickChart/CandlestickChart"
import StockSelector from "./stockSelector/StockSelector"

function Home() {
  const [requestData, setRequestData] = useState({
    ticker: "BTC-USD",
    start_date: "2019-02-01",
    end_date: "2025-03-02",
    interval: "1wk",
  })

  return (
    <div className='Home'>
      <StockSelector onSubmit={setRequestData}/>
      <CandlestickChart requestData={requestData}/>
    </div>
  )
}

export default Home