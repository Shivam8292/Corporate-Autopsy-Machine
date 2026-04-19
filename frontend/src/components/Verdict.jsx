import React from 'react';

function Verdict({ verdict }) {
    return (
        <section className="panel" style={{ borderLeft: '4px solid var(--red)' }}>
            <span className="panel-label">CORONER'S VERDICT</span>
            <p
                className="font-serif text-dim"
                style={{
                    fontSize: '15px',
                    lineHeight: '1.9',
                    fontStyle: 'italic',
                    paddingLeft: '10px'
                }}
            >
                "{verdict}"
            </p>
        </section>
    );
}

export default Verdict;
