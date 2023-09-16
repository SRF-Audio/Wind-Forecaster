import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import '../../styles/components/_wind_card.scss';

function WindCard({ data }) {
    return (
        <Card className="wind-card">
            <CardContent>
                <Typography className="text-secondary" gutterBottom>
                    Weather Data
                </Typography>
                <Typography className="text-secondary">
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
    );
}

export default WindCard;
