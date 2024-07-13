import React, { useState } from 'react';

function FormComponent({ onResult }) {
    const [url, setUrl] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        const response = await fetch('/api/audit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });
        const data = await response.json();
        onResult(data);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Website URL"
                value={url}
                onChange={e => setUrl(e.target.value)}
                required
            />
            <button type="submit">Audit</button>
        </form>
    );
}

export default FormComponent;
