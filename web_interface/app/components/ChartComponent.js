import React from 'react';
import { Bar } from 'react-chartjs-2';

function ChartComponent({ data }) {
    const chartData = {
        labels: ['Trackers', 'Cookies'],
        datasets: [
            {
                label: 'Privacy Audit Results',
                data: [data.trackers, data.cookies],
                backgroundColor: ['rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)'],
                borderColor: ['rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)'],
                borderWidth: 1
            }
        ]
    };

    return (
        <div>
            <h2>Audit Graph</h2>
            <Bar data={chartData} />
        </div>
    );
}

export default ChartComponent;
