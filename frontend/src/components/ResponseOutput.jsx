const ResponseOutput = ({ response }) => {
  return (
    <div className="response-box">
      <h3>Agent Response:</h3>
      <p>{response}</p>
    </div>
  )
}

export default ResponseOutput
