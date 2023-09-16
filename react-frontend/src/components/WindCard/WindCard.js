import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import '../../styles/components/_wind_card.scss';

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function WindCard({ data }) {
    return (
        <Card className="wind-card">
            <CardContent>
                <Typography className="text-secondary" gutterBottom>
                    Weather Data for {formatDate(data.time)}
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
