import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
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
        const response = await fetch(`${BACKEND_URL}/weather`);
        const result = await response.json();

        if (result.latitude && result.longitude) {
          setData(result);
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
            transition: 'transform 0.3s', // Transition effect for smooth scaling
            '&:hover': {
              transform: 'scale(1.05)'  // On hover, scale the card to 105% its original size
            }
          }}>
            <CardContent>
              <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                Weather Data
              </Typography>
              <Typography sx={{ mb: 1.5 }} color="text.secondary">
                Coordinates
              </Typography>
              <Typography variant="h5" component="div">
                Lat {data.latitude} Long {data.longitude}
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
