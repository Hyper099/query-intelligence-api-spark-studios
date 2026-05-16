import { useState } from 'react'

const SAMPLE_QUERY = 'Find battery technology startups in Southeast Asia'

export default function QueryForm({ onSubmit, isLoading, error }) {
  const [query, setQuery] = useState(SAMPLE_QUERY)

  function handleSubmit(event) {
    event.preventDefault()
    if (!query.trim() || isLoading) return
    onSubmit(query)
  }

  return (
    <form onSubmit={handleSubmit} className="border border-neutral-800 bg-neutral-950 p-5">
      <label htmlFor="query" className="mb-3 block text-sm font-medium text-neutral-300">
        Research query
      </label>
      <textarea
        id="query"
        rows={5}
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        placeholder={SAMPLE_QUERY}
        className="min-h-36 w-full resize-y border border-neutral-800 bg-black p-4 text-base leading-7 text-white outline-none transition placeholder:text-neutral-600 focus:border-neutral-500"
      />

      <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <p className="min-h-5 text-sm text-neutral-500">
          {error ? <span className="text-neutral-200">{error}</span> : 'Claude extracts industry, region, company type, keywords, and confidence.'}
        </p>
        <button
          type="submit"
          disabled={isLoading || !query.trim()}
          className="border border-white bg-white px-5 py-2.5 text-sm font-medium text-black transition hover:bg-neutral-200 disabled:cursor-not-allowed disabled:border-neutral-700 disabled:bg-neutral-900 disabled:text-neutral-500"
        >
          {isLoading ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>
    </form>
  )
}
