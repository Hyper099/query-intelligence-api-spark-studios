export default function ResultsPanel({ result }) {
  const data = result.structured_data

  return (
    <section className="border border-neutral-800 bg-neutral-950 p-5">
      <SectionTitle title="Structured intelligence" />

      <div className="mt-5 grid gap-4 md:grid-cols-2">
        <Field label="Original query" value={result.query} wide />
        <Field label="Normalized query" value={result.normalized_query} wide />
        <Field label="Industry" value={data.industry || 'Not detected'} />
        <Field label="Region" value={data.region || 'Not detected'} />
        <Field label="Company type" value={data.company_type || 'Not detected'} />
        <Field label="Confidence score" value={formatConfidence(data.confidence_score)} />
      </div>

      <div className="mt-5">
        <p className="text-xs font-medium uppercase tracking-[0.16em] text-neutral-500">Keywords</p>
        <div className="mt-3 flex flex-wrap gap-2">
          {data.keywords?.length ? (
            data.keywords.map((keyword) => (
              <span key={keyword} className="border border-neutral-700 px-2.5 py-1 text-sm text-neutral-200">
                {keyword}
              </span>
            ))
          ) : (
            <span className="text-sm text-neutral-500">No keywords returned</span>
          )}
        </div>
      </div>
    </section>
  )
}

function Field({ label, value, wide = false }) {
  return (
    <div className={wide ? 'md:col-span-2' : ''}>
      <p className="text-xs font-medium uppercase tracking-[0.16em] text-neutral-500">{label}</p>
      <p className="mt-2 break-words text-sm leading-6 text-neutral-100">{value}</p>
    </div>
  )
}

function SectionTitle({ title }) {
  return <h2 className="text-lg font-semibold tracking-tight text-white">{title}</h2>
}

function formatConfidence(value) {
  if (typeof value !== 'number') return 'Not available'
  return `${Math.round(value * 100)}%`
}
