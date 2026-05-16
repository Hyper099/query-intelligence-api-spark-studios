export default function HistorySidebar({ history, onSelect }) {
  return (
    <aside className="hidden w-72 shrink-0 border-r border-neutral-800 pr-6 lg:block">
      <div className="sticky top-8">
        <h2 className="text-sm font-semibold uppercase tracking-[0.18em] text-neutral-500">
          Recent queries
        </h2>
        <div className="mt-5 space-y-2">
          {history.length ? (
            history.map((item) => (
              <button
                key={item.id}
                type="button"
                onClick={() => onSelect(item)}
                className="w-full border border-neutral-800 p-3 text-left transition hover:border-neutral-600 hover:bg-neutral-900"
              >
                <p className="line-clamp-2 text-sm leading-5 text-neutral-200">{item.query}</p>
                <p className="mt-2 text-xs text-neutral-500">{item.structured_data?.region || 'No region'}</p>
              </button>
            ))
          ) : (
            <p className="text-sm leading-6 text-neutral-500">
              Submitted queries will appear here during this session.
            </p>
          )}
        </div>
      </div>
    </aside>
  )
}
