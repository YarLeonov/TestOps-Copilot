interface ResultTableProps {
  testCases: string[];
}

function ResultTable({ testCases }: ResultTableProps) {
  if (!testCases.length) {
    return <div className="empty-block">Тест-кейсы еще не сгенерированы</div>;
  }

  return (
    <div className="table-wrapper">
      <table className="table">
        <thead>
          <tr>
            <th style={{ width: "90px" }}>ID</th>
            <th>Название / описание</th>
          </tr>
        </thead>
        <tbody>
          {testCases.map((tc) => {
            const [id, ...rest] = tc.split(":");
            const title = rest.join(":").trim() || id;
            return (
              <tr key={tc}>
                <td>{id}</td>
                <td>{title}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default ResultTable;
