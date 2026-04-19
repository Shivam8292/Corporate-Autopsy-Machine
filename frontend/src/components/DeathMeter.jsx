import React, { useState, useEffect } from 'react';

function DeathMeter({ score, causeOfDeath, animate }) {
    const [currentScore, setCurrentScore] = useState(0);

    const radius = 52;
    const circumference = 2 * Math.PI * radius;

    useEffect(() => {
        if (animate) {
            let start = 0;
            const duration = 1000;
            const increment = score / (duration / 20);

            const timer = setInterval(() => {
                start += increment;
                if (start >= score) {
                    setCurrentScore(score);
                    clearInterval(timer);
                } else {
                    setCurrentScore(Math.floor(start));
                }
            }, 20);

            return () => clearInterval(timer);
        }
    }, [score, animate]);

    const offset = circumference - (currentScore / 100) * circumference;

    const getColor = (s) => {
        if (s > 75) return 'var(--red)';
        if (s > 50) return '#ff8c00';
        return '#ffd700';
    };

    return (
        <div className="panel" style={{ textAlign: 'center' }}>
            <span className="panel-label">MORTALITY PROBABILITY</span>

            <div style={{ position: 'relative', width: '150px', height: '150px', margin: '0 auto' }}>
                <svg width="150" height="150" viewBox="0 0 150 150" style={{ transform: 'rotate(-90deg)' }}>
                    <circle
                        cx="75"
                        cy="75"
                        r={radius}
                        stroke="#111"
                        strokeWidth="11"
                        fill="transparent"
                    />
                    <circle
                        cx="75"
                        cy="75"
                        r={radius}
                        stroke={getColor(currentScore)}
                        strokeWidth="11"
                        fill="transparent"
                        strokeDasharray={circumference}
                        style={{
                            strokeDashoffset: offset,
                            transition: 'stroke-dashoffset 0.1s linear, stroke 0.3s ease'
                        }}
                        strokeLinecap="round"
                    />
                </svg>
                <div style={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    fontSize: '28px',
                    fontWeight: 'bold',
                    color: getColor(currentScore)
                }}>
                    {currentScore}%
                </div>
            </div>

            <div style={{ marginTop: '20px' }}>
                <p className="text-dim" style={{ fontSize: '10px', letterSpacing: '2px', marginBottom: '4px' }}>CAUSE OF DEATH</p>
                <h2 className="font-serif text-red" style={{ fontSize: '1.2rem', textTransform: 'uppercase' }}>
                    {causeOfDeath || "UNKNOWN CRITICAL FAILURE"}
                </h2>
            </div>
        </div>
    );
}

export default DeathMeter;
