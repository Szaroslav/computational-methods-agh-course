import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faChessKnight } from '@fortawesome/free-solid-svg-icons'
import './Search.css';

function Search(props) {
    const [query, setQuery] = useState('');

    function handleQuery(event) {
        setQuery(event.target.value);
    }

    function handleSearch(event) {
        event.preventDefault();

        console.log(`http://localhost:8000/api/search?q=${encodeURIComponent(query)}&k=25`);
        fetch(`http://localhost:8000/api/search?q=${encodeURIComponent(query)}&k=25`)
            .then(response => response.json())
            .then(json => props.updateSearchData(json))
            .catch(error => console.error(error));
    }

    return (
        <div className="search-container">
            <h1><FontAwesomeIcon icon={ faChessKnight } /> Chess Search</h1>
            <form onSubmit={ handleSearch } className="search-form">
                <input type="search" value={ query } onChange={ handleQuery } className="search-input"/>
                <input type="submit" value="Search" className="search-button" />
            </form>
        </div>
    );
}

export default Search;
