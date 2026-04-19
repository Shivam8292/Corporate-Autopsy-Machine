import React from 'react';

function FailureDNA({ factors, visible }) {
    return (
        <section className="panel">
            <span className="panel-label">⬡ FAILURE DNA BREAKDOWN</span>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                {(factors || []).map((item, i) => (
                    <div key={i} style={{ animation: `fadeIn 0.5s ease-out ${i * 0.15}s both` }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '11px' }}>
                            <span className="text-secondary">{item.factor.toUpperCase()}</span>
                            <span className="text-red">{item.weight}%</span>
                        </div>

                        <div style={{ height: '6px', background: '#111', width: '100%', position: 'relative' }}>
                            <div
                                style={{
                                    height: '100%',
                                    background: 'linear-gradient(90deg, var(--red-dim), var(--red))',
                                    width: visible ? `${item.weight}%` : '0%',
                                    transition: `width 1s cubic-bezier(0.17, 0.67, 0.83, 0.67) ${i * 0.15}s`,
                                    boxShadow: '0 0 8px rgba(255, 45, 45, 0.3)'
                                }}
                            />
                        </div>

                        <p className="text-dim" style={{ fontSize: '10px', marginTop: '6px', fontStyle: 'italic' }}>
                            {item.detail}
                        </p>
                    </div>
                ))}
            </div>
        </section>
    );
}

export default FailureDNA;
