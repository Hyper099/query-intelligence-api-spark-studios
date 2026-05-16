import { useMemo, useState } from 'react'

export default function JsonViewer({ data }) {
  const [copied, setCopied] = useState(false)
  const formattedJson = useMemo(() => JSON.stringify(data, null, 2), [data])

  async function copyJson() {
    await navigator.clipboard.writeText(formattedJson)
    setCopied(true)
    window.setTimeout(() => setCopied(false), 1200)
  }

  return (
    <section className="border border-neutral-800 bg-black">
      <div className="flex items-center justify-between border-b border-neutral-800 px-5 py-4">
        <h2 className="text-lg font-semibold tracking-tight text-white">Raw JSON</h2>
        <button
          type="button"
          onClick={copyJson}
          className="border border-neutral-700 px-3 py-1.5 text-xs font-medium text-neutral-200 transition hover:border-neutral-400 hover:text-white"
        >
          {copied ? 'Copied' : 'Copy JSON'}
        </button>
      </div>
      <pre className="max-h-[700px] overflow-auto p-5 font-mono text-xs leading-6 text-neutral-300">
        {formattedJson}
      </pre>
    </section>
  )
}
