import React, { useState, useEffect } from 'react';
import ResponsiveAppBar from './components/AppBar/AppBar';
import Arrow from './components/Arrow/Arrow';
import WindCard from './components/WindCard/WindCard';
import './styles/App.scss';

function App() {
  const [data, setData] = useState([]);
  const [sliderValue, setSliderValue] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const endpoint = "/api/hourly";
        const response = await fetch(endpoint);
        const result = await response.json();
        if (Array.isArray(result) && result.length) {
          setData(result);
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
      <div className="CardContainer">
        <WindCard data={data[sliderValue] || {}} />
      </div>
      <header className="App-header">
        {data === null && <p>Loading...</p>}
        {data.length === 0 && <p>No backend connection or no data available</p>}
      </header>
      <div className="ArrowContainer">
        <div className="InnerContainer">
          {/* Modification here: */}
          <Arrow direction={(data[sliderValue]?.winddirection + 180) % 360 - 90 || -90} />
          <div className="SliderContainer">
            <input
              className="CustomSlider"
              type="range"
              min="0"
              max={data.length - 1}
              value={sliderValue}
              onChange={e => setSliderValue(Number(e.target.value))}
            />
            <div className="SliderLabels">
              {data.map((item, index) => {
                const date = new Date(item.time);
                const hour = date.getHours();
                if (hour % 6 === 0) {
                  const displayHour = hour === 0 ? "12AM" : hour === 12 ? "12PM" : hour < 12 ? `${hour}AM` : `${hour - 12}PM`;
                  return (
                    <span key={index} style={{ left: `${(index / (data.length - 1)) * 100}%` }}>
                      {displayHour}
                    </span>
                  );
                }
                return null;
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
