import React, { useState, useEffect } from 'react';
import ResponsiveAppBar from './components/AppBar/AppBar';
import WindCard from './components/WindCard/WindCard';
import './styles/app.scss';

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

    const fetchData = async () => {
      try {
        const response = await fetch(`${BACKEND_URL}/hourly`);
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
        {data.length > 0 ? (
          data.map((forecast, index) => <WindCard key={index} data={forecast} />)
        ) : (
          data === null && <p>Loading...</p>
        )}

        {data.length === 0 && <p>No backend connection or no data available</p>}
      </header>
    </div>
  );
}

export default App;
