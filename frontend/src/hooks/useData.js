import {useState, useEffect} from "react"
import axios from "axios"

function useData(url, requestData) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)


  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const response = await axios.post(url, requestData)
        setData(response.data)
        setLoading(false)
      } catch (err) {
        setError(err)
        setLoading(false)
      }
    }

    fetchData()
  }, [url, requestData])

  return {data, loading, error}
}

export default useData
