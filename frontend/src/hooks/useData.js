import {useState, useEffect} from "react";
import axios from "axios";

function useData(url, requestData) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);


  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);  // ustawienie statusu ładowania
        const response = await axios.post(url, requestData);
        setData(response.data);  // zapisanie danych do stanu
        setLoading(false);  // zakończenie ładowania
      } catch (err) {
        setError(err);  // zapisanie błędu
        setLoading(false);  // zakończenie ładowania
      }
    };

    fetchData();
  }, [url]);  // uruchamianie efektu za każdym razem, gdy zmienia się URL lub requestData

  return {data, loading, error};
}

export default useData;
