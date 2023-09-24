import React, { useState, useEffect } from 'react';
import ResponsiveAppBar from './components/AppBar/AppBar';
import Arrow from './components/Arrow/Arrow';
import './styles/App.scss';

function App() {
  const [data, setData] = useState([]);
  const [sliderValue, setSliderValue] = useState(0);

  useEffect(() => {

    const fetchData = async () => {
      try {
        const endpoint = "/api/hourly";
        console.log("Fetching data from:", endpoint);
        const response = await fetch(endpoint);

        // Debugging statements
        console.log("HTTP Status:", response.status);
        console.log("Full Response:", response);
        console.log("Response Headers:", response.headers);

        const result = await response.json();

        if (Array.isArray(result) && result.length) {
          setData(result);
          console.log("Data fetched:", result);
        } else {
          setData([]);
        }

      } catch (error) {
        console.error("Error fetching data:", error);
        setData([]);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="App">
      <ResponsiveAppBar />
      <header className="App-header">
        {data === null && <p>Loading...</p>}
        {data.length === 0 && <p>No backend connection or no data available</p>}
      </header>
      <div className="ArrowContainer">
        <Arrow direction={data[sliderValue]?.winddirection || 0} />
        <input
          type="range"
          min="0"
          max={data.length - 1}
          value={sliderValue}
          onChange={e => setSliderValue(Number(e.target.value))}
        />
      </div>
    </div>
  );
}

export default App;
