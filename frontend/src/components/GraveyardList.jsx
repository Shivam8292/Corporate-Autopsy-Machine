import React from 'react';

function GraveyardList({ failures }) {
    return (
        <section className="panel">
            <span className="panel-label">☠ SIMILAR CORPSES IN THE GRAVEYARD</span>

            <div style={{ display: 'flex', flexDirection: 'column' }}>
                {(failures || []).map((corp, i) => (
                    <div key={i}>
                        <div style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'baseline',
                            padding: '12px 0'
                        }}>
                            <div style={{ flex: 1 }}>
                                <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px' }}>
                                    <span style={{ color: '#fff', fontWeight: 'bold' }}>{corp.name}</span>
                                    <span className="text-dim" style={{ fontSize: '10px' }}>({corp.year})</span>
                                </div>
                                <p className="text-dim" style={{ fontSize: '11px', mt: '4px', maxWidth: '80%' }}>
                                    {corp.reason}
                                </p>
                            </div>

                            <div style={{ textAlign: 'right' }}>
                                <div className="text-red" style={{ fontSize: '20px', fontWeight: 'bold' }}>{corp.similarity}%</div>
                                <div className="text-dim" style={{ fontSize: '8px', letterSpacing: '1px' }}>MATCH</div>
                            </div>
                        </div>
                        {i < failures.length - 1 && (
                            <div style={{ height: '1px', background: 'var(--border)', width: '100%' }}></div>
                        )}
                    </div>
                ))}
            </div>
        </section>
    );
}

export default GraveyardList;
