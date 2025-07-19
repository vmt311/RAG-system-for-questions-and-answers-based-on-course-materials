import { useState } from 'react'
import ChatBox from './components/ChatBox'
import api from './components/api'
import RetrievalDocs from './components/RetrievalDocs'

function App() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Здравствуйте, чем я могу вам помочь?' }
  ])
  const [loading, setLoading] = useState(false)
  const [retrievalDocs, setRetrievalDocs] = useState([])

  const handleSend = async (query) => {
    const userMessage = { sender: 'user', text: query }
    setMessages((prev) => [...prev, userMessage])
    setLoading(true)

    try {
      const response = await api.post("llm", {query})
      console.log(response)
      const { answer, retrieval_documents } = response.data
      console.log(answer)
      console.log(retrieval_documents)
      const botReply = { sender: 'bot', text:  answer}
      setRetrievalDocs(retrieval_documents)
      setMessages((prev) => [...prev, botReply])
    } catch (error) {
      setMessages(prev => [...prev, { sender: 'bot', text: error }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 p-5">
      <div className="w-full max-w-4xl bg-white rounded-2xl shadow-lg p-4 flex flex-col mx-auto">
        <h1 className="text-2xl font-bold mb-4 text-center text-black flex items-center justify-center gap-2">
          <span>Chatbot</span>
        </h1>
        <ChatBox messages={messages} onSend={handleSend} loading={loading}/>
      </div>
      {/* <div className="w-full max-w-lg bg-white rounded-2xl shadow-lg p-4 flex flex-col mx-auto">
        <h1 className="text-2xl font-bold mb-4 text-center text-black flex items-center justify-center gap-2">
          <span>Retrieval documents</span>
        </h1>
        <RetrievalDocs listDocs = {retrievalDocs} loading={loading} />
      </div> */}
    </div>

  )
}

export default App
