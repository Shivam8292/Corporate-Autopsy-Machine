import React from 'react';

function Pivots({ pivots }) {
    return (
        <section className="panel" style={{ borderColor: '#1a3a1a', background: 'rgba(0, 200, 80, 0.02)' }}>
            <span className="panel-label" style={{ color: 'var(--green)' }}>↑ PIVOTS THAT COULD HAVE SAVED IT</span>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {(pivots || []).map((pivot, i) => (
                    <div key={i} style={{ display: 'flex', gap: '12px' }}>
                        <span style={{ color: 'var(--green)', fontWeight: 'bold' }}>0{i + 1}</span>
                        <p className="text-dim" style={{ fontSize: '12px' }}>{pivot}</p>
                    </div>
                ))}
            </div>
        </section>
    );
}

export default Pivots;
