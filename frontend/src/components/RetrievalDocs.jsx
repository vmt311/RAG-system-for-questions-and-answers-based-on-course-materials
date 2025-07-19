const RetrievalDocs = ({listDocs, loading}) => {
    if (loading) {
        return (
            <div className="h-[600px] overflow-y-auto space-y-4 pr-2">
                <div className="spinner"></div>
            </div>
        )
      }

    return (
        <div className="h-[600px] overflow-y-auto space-y-4 pr-2">
            {listDocs.map((item, index) => (
            <div
                key={index}
                className={`p-4 rounded-lg shadow-md border ${
                item.flag === 'True'
                    ? 'border-green-500 bg-green-100'
                    : 'border-gray-300 bg-white'
                }`}
            >
                <p className="text-sm text-gray-500 mb-2">
                📄 <strong>Source:</strong> {item.source}
                </p>
                <p className="text-base text-gray-800 whitespace-pre-line">{item.context}</p>
                <div className="flex justify-between items-center mt-2">
                <span className="text-sm">
                    🔍 <strong>Score:</strong> {item.score.toFixed(3)}
                </span>
                <span className="text-sm">
                    ✅ <strong>Relevant:</strong> {item.flag}
                </span>
                </div>
            </div>
            ))}
        </div>
      )
}

export default RetrievalDocs;