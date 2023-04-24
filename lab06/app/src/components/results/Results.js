import React from 'react';
import './Results.css';

function Results(props) {
    return (
        <div className="results-container">
            <ul className="results-list">
                {
                    props.data
                        .map((document, i) => <li key={ i } className="results-item">{ document }</li>)
                }
            </ul>
        </div>
    );
}

export default Results;