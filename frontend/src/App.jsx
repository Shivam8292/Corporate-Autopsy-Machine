import { useState } from 'react'
import IntakeForm from './components/IntakeForm'
import LoadingScreen from './components/LoadingScreen'
import AutopsyReport from './components/AutopsyReport'
import { runAutopsy } from './api'

function App() {
  const [stage, setStage] = useState('idle'); // 'idle' | 'loading' | 'result'
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (idea) => {
    setStage('loading');
    setError(null);
    setResult(null);

    try {
      const data = await runAutopsy(idea);
      if (data.error) {
        throw new Error(data.error);
      }
      setResult(data);
      setStage('result');
    } catch (err) {
      setError(err.message);
      setStage('idle');
      console.error("Autopsy Failed:", err);
    }
  };

  const handleReset = () => {
    setStage('idle');
    setResult(null);
    setError(null);
  };

  return (
    <div className="app-container" style={{ paddingBottom: '60px' }}>
      <header style={{ padding: '60px 20px 20px', textAlign: 'center' }}>
        <p className="text-red" style={{ fontSize: '10px', letterSpacing: '4px', marginBottom: '8px' }}>
          ◆ CLASSIFIED SYSTEM ◆
        </p>
        <h1 className="font-serif" style={{ fontSize: 'clamp(2rem, 5vw, 3.5rem)', margin: '10px 0', background: 'linear-gradient(180deg, #fff, #888)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          CORPORATE AUTOPSY MACHINE
        </h1>
        <p className="text-red" style={{ fontSize: '12px', letterSpacing: '1px' }}>
          v2.1 — RAG-POWERED FAILURE INTELLIGENCE
        </p>
        <div className="divider" style={{ maxWidth: '600px', margin: '30px auto' }}></div>
      </header>

      <main style={{ maxWidth: '900px', margin: '0 auto', padding: '0 20px' }}>
        {error && (
          <div className="panel" style={{ borderColor: 'var(--red)', color: 'var(--red)', marginBottom: '20px', fontSize: '12px' }}>
            <span className="panel-label">SYSTEM ERROR</span>
            [!] ERROR: {error.toUpperCase()}
          </div>
        )}

        {stage === 'idle' && (
          <IntakeForm onSubmit={handleSubmit} loading={false} />
        )}

        {stage === 'loading' && (
          <>
            <IntakeForm onSubmit={handleSubmit} loading={true} />
            <LoadingScreen />
          </>
        )}

        {stage === 'result' && result && (
          <AutopsyReport result={result} onReset={handleReset} />
        )}
      </main>

      <footer style={{ marginTop: '60px', padding: '40px', textAlign: 'center', borderTop: '1px solid var(--border)' }}>
        <p className="text-ghost" style={{ fontSize: '10px', letterSpacing: '2px' }}>
          CORPORATE AUTOPSY MACHINE — ALL PATTERNS ARE DOCUMENTED
        </p>
      </footer>
    </div>
  )
}

export default App
