import Header from '../components/Header.jsx'
import HistorySidebar from '../components/HistorySidebar.jsx'
import JsonViewer from '../components/JsonViewer.jsx'
import MetadataPanel from '../components/MetadataPanel.jsx'
import QueryForm from '../components/QueryForm.jsx'
import ResultsPanel from '../components/ResultsPanel.jsx'
import { useQueryAnalysis } from '../hooks/useQueryAnalysis.js'

export default function QueryPage() {
  const { result, history, error, isLoading, submitQuery, selectResult } = useQueryAnalysis()

  return (
    <main className="min-h-screen bg-neutral-950 text-white">
      <div className="mx-auto flex w-full max-w-7xl gap-8 px-6 py-8 lg:px-8">
        <HistorySidebar history={history} onSelect={selectResult} />

        <section className="flex min-w-0 flex-1 flex-col gap-8">
          <Header />
          <QueryForm onSubmit={submitQuery} isLoading={isLoading} error={error} />

          {result ? (
            <div className="fade-in grid gap-6 xl:grid-cols-[1fr_0.92fr]">
              <div className="space-y-6">
                <ResultsPanel result={result} />
                <MetadataPanel metadata={result.metadata} createdAt={result.created_at} />
              </div>
              <JsonViewer data={result} />
            </div>
          ) : (
            <div className="border border-neutral-800 bg-neutral-950 p-8 text-sm text-neutral-500">
              Results will appear here after you analyze a query.
            </div>
          )}
        </section>
      </div>
    </main>
  )
}
