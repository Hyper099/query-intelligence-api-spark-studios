export default function MetadataPanel({ metadata, createdAt }) {
  return (
    <section className="border border-neutral-800 bg-neutral-950 p-5">
      <h2 className="text-lg font-semibold tracking-tight text-white">Metadata</h2>
      <dl className="mt-5 grid gap-4 sm:grid-cols-2">
        <MetadataItem label="Claude model used" value={metadata?.model} />
        <MetadataItem label="Processing latency" value={`${metadata?.processing_latency_ms ?? 0} ms`} />
        <MetadataItem label="Extraction source" value={metadata?.extraction_source} />
        <MetadataItem label="Created timestamp" value={formatDate(createdAt)} />
      </dl>
    </section>
  )
}

function MetadataItem({ label, value }) {
  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-[0.16em] text-neutral-500">{label}</dt>
      <dd className="mt-2 break-words text-sm text-neutral-100">{value || 'Not available'}</dd>
    </div>
  )
}

function formatDate(value) {
  if (!value) return 'Not available'
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'medium',
  }).format(new Date(value))
}
