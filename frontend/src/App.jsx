import { useEffect, useEffectEvent, useState } from 'react'
import StatCards from './components/features/summary/StatCards'
import './index.css'

const DESKTOP_BREAKPOINT = 1024

export default function App() {
  const [isDesktop, setIsDesktop] = useState(
    () => window.innerWidth >= DESKTOP_BREAKPOINT,
  )

  useEffect(() => {
    const handleResize = () => {
      setIsDesktop(window.innerWidth >= DESKTOP_BREAKPOINT)
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)

  }, [])

  const [summary, setSummary] = useState({
    total_income: 0,
    total_expense: 0,
    net_savings: 0,
  })

  useEffect(() => {
    async function fetchSummary() {
      try {
        const response = await fetch('/finance_tracker/summary')

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const data = await response.json()

        if (data?.summary) {
          setSummary(data.summary)
        }

      } catch (err) {
        console.error('Failed to fetch finance summary:', err)
      }
    }

    fetchSummary()
  }, [])

  return (
    <div className='app-shell'>
      {/* --- Top row: 3 metric cards --- */}
      <StatCards summary={summary} />
      {/* --- Main Body: 2 column desktop, stacked on mobile --- */}
      <main className={isDesktop ? 'body-grid' : 'body-stacked'}>
        <section className='left-col'>
          <div className='wf-box wf-sand'>CHART</div>
          <div className='wf-box wf-crimson'>FORM</div>
        </section>

        <section className='right-col'>
          <div className='wf-box wf-maroon'>TRANSACTION FEED</div>
        </section>
      </main>
    </div>
  )
}