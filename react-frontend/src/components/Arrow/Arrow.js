import React from 'react';

function Arrow({ direction = 0 }) {
    return (
        <div id="pointer" style={{ transform: `rotate(${direction}deg)` }}></div>
    );
}

export default Arrow;
