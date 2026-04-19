import React, { useState, useEffect } from 'react';
import DeathMeter from './DeathMeter';
import FailureDNA from './FailureDNA';
import GraveyardList from './GraveyardList';
import Pivots from './Pivots';
import Verdict from './Verdict';

function AutopsyReport({ result, onReset }) {
    const [showSections, setShowSections] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => setShowSections(true), 300);
        return () => clearTimeout(timer);
    }, []);

    if (!result) return null;

    return (
        <div style={{ animation: 'fadeIn 0.8s ease-out' }}>
            <div className="grid-2">
                <DeathMeter
                    score={result.deathScore}
                    causeOfDeath={result.causeOfDeath}
                    animate={showSections}
                />
                <Verdict verdict={result.verdict} />
            </div>

            <div style={{ marginTop: '20px' }}>
                <FailureDNA factors={result.failureDNA} visible={showSections} />
            </div>

            <div style={{ marginTop: '20px' }}>
                <GraveyardList failures={result.similarFailures} />
            </div>

            <div style={{ marginTop: '20px' }}>
                <Pivots pivots={result.pivots} />
            </div>

            <div style={{ textAlign: 'center', margin: '40px 0' }}>
                <button
                    onClick={onReset}
                    style={{
                        background: 'transparent',
                        border: 'none',
                        color: 'var(--text-ghost)',
                        fontSize: '12px',
                        textDecoration: 'underline',
                        letterSpacing: '2px'
                    }}
                    onMouseOver={(e) => e.target.style.color = 'var(--red)'}
                    onMouseOut={(e) => e.target.style.color = 'var(--text-ghost)'}
                >
                    {"← NEW AUTOPSY"}
                </button>
            </div>
        </div>
    );
}

export default AutopsyReport;
