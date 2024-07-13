import React from 'react';
import FormComponent from './components/FormComponent';
import ResultComponent from './components/ResultComponent';
import ChartComponent from './components/ChartComponent';
import './styles.css';

function MainComponent() {
    const [result, setResult] = React.useState(null);

    const handleResult = (data) => {
        setResult(data);
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>Data Guardian</h1>
                <FormComponent onResult={handleResult} />
                {result && <ResultComponent result={result} />}
                {result && <ChartComponent data={result} />}
            </header>
        </div>
    );
}

export default MainComponent;
