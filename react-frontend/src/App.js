import React, { useState, useEffect } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import ResponsiveAppBar from './components/AppBar/AppBar'

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

    const fetchData = async () => {
      try {
        const response = await fetch(`${BACKEND_URL}/hourly`);
        const result = await response.json();

        if (Array.isArray(result) && result.length) {
          setData(result[0]);  // assuming you want the first object in the returned array
        } else {
          setData("error");
        }

      } catch (error) {
        setData("error");
      }
    };

    fetchData();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <ResponsiveAppBar />

        {data && data !== "error" && (
          <Card sx={{
            minWidth: 275,
            mt: 3,
            background: 'linear-gradient(90deg, hsla(33, 100%, 53%, 1) 0%, hsla(58, 100%, 68%, 1) 100%)',
            transition: 'transform 0.3s',
            '&:hover': {
              transform: 'scale(1.05)'
            }
          }}>
            <CardContent>
              <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                Weather Data
              </Typography>
              <Typography sx={{ mb: 1.5 }} color="text.secondary">
                Wind Information
              </Typography>
              <Typography variant="h5" component="div">
                Wind Direction: {data.winddirection}°
              </Typography>
              <Typography variant="h5" component="div">
                Wind Gusts: {data.windgusts} m/s
              </Typography>
              <Typography variant="h5" component="div">
                Wind Speed: {data.windspeed} m/s
              </Typography>
            </CardContent>
          </Card>
        )}

        {data === null && <p>Loading...</p>}
        {data === "error" && <p>No backend connection</p>}
      </header>
    </div>
  );
}

export default App;
