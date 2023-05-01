import React, { useState } from 'react';
import './style.css'; // import the CSS file

function Chatbot() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const handleChange = (event) => {
    setMessage(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://localhost:5000/search');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        const res = JSON.parse(xhr.responseText);
        // console.log(">>>>>", res)
        setResponse(res);
        setMessage('');
      }
    };
    xhr.send(JSON.stringify({ search_prompt: message }));
  };

  return (
    <div className="chatbot">
      <h1><b>California DMV Help</b></h1><hr></hr>
      <div className="chatbot__conversation">
        <div className="chatbot__bubble chatbot__bubble--user">
          <textarea
            value={message}
            onChange={handleChange}
            placeholder="Type your message here..."
          />
        </div>
        <div className="chatbot__button">
          <button onClick={handleSubmit}>Send</button>
        </div><br></br>
        {response && (
          <div className="chatbot__bubble chatbot__bubble--bot">
            {response}
          </div>
        )}
      </div>
    </div>
  );
}

export default Chatbot;

