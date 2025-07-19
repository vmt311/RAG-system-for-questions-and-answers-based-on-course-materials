import { useState, useRef, useEffect } from 'react'
import Message from './Message'
import api from './api'

const ChatBox = ({ messages, onSend, loading }) => {
  const [input, setInput] = useState('')
  const chatEndRef = useRef(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim() === '') return
    onSend(input.trim())
    setInput('')
  }

  // Tự động cuộn xuống cuối khi có tin nhắn mới
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  // Xu ly giong noi
  const handleMicroClick = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      const audioChunks = []

      mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data)
      }

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav'})
        const formData = new FormData()
        formData.append('file', audioBlob, 'recording.wav')

        try {
          const response = await api.post("/speech-to-text", formData, {
            headers: { 'Content-Type': 'multupart/form-data'}
          })

          const transcribedText = response.data.text
          console.log(transcribedText)
          // onSend(transcribedText)
          setInput(transcribedText)
        } catch (err) {
          console.error('Speech-to-text error:', err)
        }
      }

      mediaRecorder.start()
      setTimeout(() => {
        mediaRecorder.stop()
        stream.getTracks().forEach(track => track.stop())
      }, 5000)
    } catch (err) {
      alert('fail to connect micro!')
      console.error(err)
    }
  }

  return (
    <div className="flex flex-col h-[600px]">
      <div className="flex-1 overflow-y-auto mb-2 space-y-2 p-2 bg-gray-50 rounded-lg">
        {messages.map((msg, index) => (
          <Message key={index} sender={msg.sender} text={msg.text} />
        ))}

        {/* Hiển thị biểu tượng loading từ bot nếu đang phản hồi */}
        {loading && <Message sender="bot" loading />}

        <div ref={chatEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="flex">
        <input
          type="text"
          className="flex-1 border 
                    rounded-l-lg bg-gray-300 
                    text-black px-3 py-2 
                    focus:outline-none"
          placeholder="Введите вопрос..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded-r-lg hover:bg-blue-600 cursor-pointer"
        >
          Отправить
        </button>
        <button
          type="button"
          onClick={handleMicroClick}
          className="bg-red-500 text-white px-3 py-2 rounded-lg hover:bg-red-600 ml-1 cursor-pointer"
          title="Голосовой ввод"
        >
          🎤
        </button>
      </form>
    </div>
  )
}

export default ChatBox
