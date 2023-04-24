import React, { useState } from 'react';
import './App.css';
import Search from './components/search/Search';
import Results from './components/results/Results';

function App() {
    const [data, setData] = useState([]);

    function handleSearchUpdate(data) {
        setData(data);
    }

    return (
        <div className="search-application">
            <Search updateSearchData={ handleSearchUpdate }/>
            <Results data={ data }/>
        </div>
    );
}

export default App;
