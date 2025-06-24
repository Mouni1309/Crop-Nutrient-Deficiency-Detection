import React, { useState } from 'react';
import './App.css';

function App() {
  const handleChat = async () => {
    if (!chatMessage.trim()) {
      alert('Please enter a message to chat!');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: chatMessage }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setChatResponse(data.response);
      setChatMessage('');
    } catch (error) {
      console.error('Error during chat:', error);
      setChatResponse('Error getting response. Please try again.');
    }
  };
  const [selectedFile, setSelectedFile] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [info, setInfo] = useState(null);
  const [chatMessage, setChatMessage] = useState('');
  const [chatResponse, setChatResponse] = useState('');
  const [imagePreview, setImagePreview] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    } else {
      setImagePreview(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select an image first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setPrediction(data.prediction);
      setInfo(data.info);
    } catch (error) {
      console.error('Error uploading image:', error);
      setPrediction('Error predicting. Please try again.');
      setInfo(null);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Crop Disease Detector</h1>
      </header>
      <main>
        <div className="upload-section">
          <input type="file" accept="image/*" onChange={handleFileChange} />
          <button onClick={handleUpload}>Upload and Predict</button>
        </div>
        {imagePreview && (
          <div className="image-preview">
            <h2>Image Preview:</h2>
            <img src={imagePreview} alt="Preview" style={{ maxWidth: '300px', maxHeight: '300px' }} />
          </div>
        )}
        {prediction && (
          <div className="prediction-result">
            <h2>Prediction:</h2>
            <p>{prediction}</p>
          </div>
        )}
        {info && (
          <div className="info-result">
            <h2>Detailed Information:</h2>
            <p>{info}</p>
          </div>
        )}
        <div className="chat-section">
          <h2>Chat with AI Expert</h2>
          <input
            type="text"
            value={chatMessage}
            onChange={(e) => setChatMessage(e.target.value)}
            placeholder="Ask about crop diseases..."
          />
          <button onClick={handleChat}>Send Message</button>
          {chatResponse && (
            <div className="chat-response">
              <h3>AI Response:</h3>
              <p>{chatResponse}</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;