import React from 'react';

function ResultComponent({ result }) {
    return (
        <div>
            <h2>Audit Result</h2>
            <p>URL: {result.url}</p>
            <p>Trackers: {result.trackers}</p>
            <p>Cookies: {result.cookies}</p>
        </div>
    );
}

export default ResultComponent;
