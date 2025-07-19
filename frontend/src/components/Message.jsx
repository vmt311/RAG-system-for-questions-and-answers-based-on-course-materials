const Message = ({ sender, text, loading }) => {
    const isUser = sender === 'user'

    if (loading && !isUser) {
      return (
        <div className="flex justify-start">
          <div className="px-4 py-2 rounded-xl max-w-xs bg-gray-300 text-black flex items-center space-x-1">
            <span className="dot animate-bounce delay-0">.</span>
            <span className="dot animate-bounce delay-150">.</span>
            <span className="dot animate-bounce delay-300">.</span>
          </div>
        </div>
      )
    }
    
    // Tách đoạn văn theo dòng trống
    const paragraphs = text.split(/\n\s*\n/)

    return (
      <div lang="ru" className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
        <div className={`px-4 py-2 rounded-xl max-w-5xl text-base leading-relaxed
            ${isUser ? 'bg-blue-500 text-white' : 'bg-gray-300 text-black'}`}>
          {paragraphs.map((para, idx) => (
          <p key={idx} className="mb-2 text-justify whitespace-pre-line hyphens-auto break-words">
            {para.trim()}
          </p>
        ))}
        </div>
      </div>
    )
  }
  
  export default Message
  