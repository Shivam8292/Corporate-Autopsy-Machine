import React, { useState } from 'react';

const EXAMPLES = [
    "Uber for dog walkers",
    "AI-powered meal kit delivery",
    "Crypto freelance marketplace",
    "Premium juice subscription boxes",
    "Social network for book readers"
];

function IntakeForm({ onSubmit, loading }) {
    const [idea, setIdea] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        if (idea.trim() && !loading) {
            onSubmit(idea);
        }
    };

    return (
        <section className="panel">
            <span className="panel-label">SUBJECT INTAKE</span>
            <p className="text-dim" style={{ fontSize: '12px', marginBottom: '16px' }}>
                {">"} DESCRIBE YOUR STARTUP IDEA. THE MACHINE SHOWS NO MERCY.
            </p>

            <form onSubmit={handleSubmit}>
                <textarea
                    value={idea}
                    onChange={(e) => setIdea(e.target.value)}
                    placeholder="ENTER STARTUP CONCEPT..."
                    style={{ width: '100%', minHeight: '120px', resize: 'vertical', marginBottom: '16px' }}
                    disabled={loading}
                />

                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '20px' }}>
                    {EXAMPLES.map((ex, i) => (
                        <div
                            key={i}
                            onClick={() => !loading && setIdea(ex)}
                            className="text-ghost"
                            style={{
                                cursor: 'pointer',
                                border: '1px solid var(--text-dim)',
                                padding: '4px 8px',
                                fontSize: '10px',
                                transition: 'all 0.2s ease',
                                background: 'rgba(255,45,45,0.05)'
                            }}
                            onMouseOver={(e) => e.target.style.color = 'var(--red)'}
                            onMouseOut={(e) => e.target.style.color = 'var(--text-ghost)'}
                        >
                            {ex}
                        </div>
                    ))}
                </div>

                <button
                    type="submit"
                    disabled={loading || !idea.trim()}
                    style={{ width: '100%', padding: '16px', fontSize: '14px', fontWeight: 'bold' }}
                >
                    {loading ? "⚰ ANALYZING..." : "⚰ RUN AUTOPSY"}
                </button>
            </form>

            <p style={{ marginTop: '12px', textAlign: 'center', fontSize: '10px' }} className="text-dim">
                POWERED BY RAG + LOCAL EMBEDDINGS
            </p>
        </section>
    );
}

export default IntakeForm;
