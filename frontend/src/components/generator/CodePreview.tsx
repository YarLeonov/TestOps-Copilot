import { useState } from "react";
import type { CodeBundle } from "../../api/generation";

interface CodePreviewProps {
  bundles: CodeBundle[];
}

function CodePreview({ bundles }: CodePreviewProps) {
  const [selectedIndex, setSelectedIndex] = useState(0);

  if (!bundles.length) {
    return <div className="empty-block">Код автотестов еще не сгенерирован</div>;
  }

  const selected = bundles[selectedIndex] ?? bundles[0];

  return (
    <div className="code-preview">
      <div className="code-preview-header">
        <select
          className="select"
          value={selectedIndex}
          onChange={(e) => setSelectedIndex(Number(e.target.value))}
        >
          {bundles.map((b, idx) => (
            <option key={b.name + idx} value={idx}>
              {b.name}
            </option>
          ))}
        </select>

        <button
          type="button"
          className="btn btn-ghost"
          onClick={() => {
            void navigator.clipboard.writeText(selected.content);
          }}
        >
          Копировать
        </button>
      </div>

      <pre className="code-block">
        <code>{selected.content}</code>
      </pre>
    </div>
  );
}

export default CodePreview;
