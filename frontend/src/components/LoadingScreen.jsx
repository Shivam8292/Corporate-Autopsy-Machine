import React, { useState, useEffect } from 'react';

const MESSAGES = [
    "⚰️ Searching startup graveyard...",
    "🔬 Analyzing failure DNA...",
    "📊 Cross-referencing post-mortems...",
    "🧬 Identifying cause of death...",
    "📋 Preparing autopsy report..."
];

function LoadingScreen() {
    const [index, setIndex] = useState(0);
    const [displayText, setDisplayText] = useState("");
    const [charIndex, setCharIndex] = useState(0);

    useEffect(() => {
        const messageInterval = setInterval(() => {
            setIndex((prev) => (prev + 1) % MESSAGES.length);
            setCharIndex(0);
        }, 1400);

        return () => clearInterval(messageInterval);
    }, []);

    useEffect(() => {
        const currentMessage = MESSAGES[index];
        if (charIndex < currentMessage.length) {
            const timeout = setTimeout(() => {
                setDisplayText(currentMessage.substring(0, charIndex + 1));
                setCharIndex(charIndex + 1);
            }, 30);
            return () => clearTimeout(timeout);
        }
    }, [index, charIndex]);

    return (
        <div className="panel" style={{ textAlign: 'center', padding: '60px 20px', minHeight: '200px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <div className="text-red" style={{ fontSize: '20px', marginBottom: '16px', minHeight: '30px' }}>
                {displayText}
            </div>
            <p className="text-dim" style={{ fontSize: '10px', letterSpacing: '2px' }}>
                CROSS-REFERENCING FAILURE DATABASE...
            </p>

            <div style={{ marginTop: '24px', height: '2px', width: '100%', background: '#111', overflow: 'hidden' }}>
                <div
                    className="scanline-bar"
                    style={{
                        height: '100%',
                        width: '30%',
                        background: 'var(--red)',
                        boxShadow: '0 0 10px var(--red)',
                        animation: 'loading-bar 1.5s infinite linear'
                    }}
                />
            </div>

            <style>{`
        @keyframes loading-bar {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(400%); }
        }
      `}</style>
        </div>
    );
}

export default LoadingScreen;
