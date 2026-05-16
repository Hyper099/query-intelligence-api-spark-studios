import { useState } from 'react'
import { analyzeQuery } from '../services/queryApi.js'

export function useQueryAnalysis() {
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  async function submitQuery(query) {
    setIsLoading(true)
    setError('')

    try {
      const data = await analyzeQuery(query)
      setResult(data)
      setHistory((items) => [data, ...items].slice(0, 8))
    } catch (err) {
      const message = err.response?.data?.detail || 'Unable to analyze the query. Please try again.'
      setError(Array.isArray(message) ? 'Please enter a valid research query.' : message)
    } finally {
      setIsLoading(false)
    }
  }

  return {
    result,
    history,
    error,
    isLoading,
    submitQuery,
    selectResult: setResult,
  }
}
