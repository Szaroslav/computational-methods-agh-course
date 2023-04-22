import React, { useState } from 'react';
import './Search.css';

function Search(props) {
    const [query, setQuery] = useState('');

    function handleQuery(event) {
        setQuery(event.target.value);
    }

    function handleSearch(event) {
        event.preventDefault();

        console.log(`http://localhost:9001/api/search?q=${encodeURIComponent(query)}&k=25`);
        fetch(`http://localhost:9001/api/search?q=${encodeURIComponent(query)}&k=25`)
            .then(response => response.json())
            .then(json => props.updateSearchData(json))
            .catch(error => console.error(error));
    }

    return (
        <div className="search-container">
            <h1>Chess search</h1>
            <form onSubmit={ handleSearch } className="search-form">
                <input type="search" value={ query } onChange={ handleQuery }/>
                <input type="submit" value="Search" />
            </form>
        </div>
    );
}

export default Search;
