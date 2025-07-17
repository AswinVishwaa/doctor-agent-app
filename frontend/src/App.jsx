import React, { useState } from 'react'
import PromptInput from './components/PromptInput'
import ResponseOutput from './components/ResponseOutput'

const App = () => {
  const [response, setResponse] = useState('')

  return (
    <div className="app-container">
      <h1>🧠 Doctor Assistant Agent</h1>
      <PromptInput setResponse={setResponse} />
      <ResponseOutput response={response} />
    </div>
  )
}

export default App
