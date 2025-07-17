import React, { useState } from 'react'
import axios from 'axios'

const PromptInput = ({ setResponse }) => {
  const [prompt, setPrompt] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await axios.post('http://localhost:8000/agent/prompt', { prompt })
      setResponse(res.data.response)
    } catch (err) {
      setResponse('Error: Could not process prompt')
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} rows={4} placeholder="Type your request..." />
      <button type="submit">Send</button>
    </form>
  )
}

export default PromptInput
