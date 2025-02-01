from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def get_ui():
    html_content = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>Voice Assistant</title>
        <style>
          .controls { margin: 20px 0; }
          #status { color: #666; margin: 10px 0; }
          #result { margin: 20px 0; padding: 10px; background: #f0f0f0; }
        </style>
      </head>
      <body>
        <h1>Voice Assistant</h1>
        <div class="controls">
          <button id="recordButton">Start Recording</button>
          <p id="status">Click to start recording</p>
        </div>
        <div id="result"></div>

        <script>
          let mediaRecorder;
          let audioChunks = [];
          const recordButton = document.getElementById('recordButton');
          const status = document.getElementById('status');

          async function setupRecording() {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = (event) => {
              audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
              const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
              await processAudioInteraction(audioBlob);
            };
          }

          recordButton.onclick = () => {
            if (mediaRecorder?.state === 'inactive') {
              audioChunks = [];
              mediaRecorder.start();
              recordButton.textContent = 'Stop Recording';
              status.textContent = 'Recording...';
            } else {
              mediaRecorder.stop();
              recordButton.textContent = 'Start Recording';
              status.textContent = 'Processing...';
            }
          };

          async function processAudioInteraction(audioBlob) {
            try {
              // Send audio for STT
              const formData = new FormData();
              formData.append('audio', audioBlob, 'recording.wav');
              const sttResponse = await fetch('http://127.0.0.1:8000/ml/speech-to-text', {
                method: 'POST',
                body: formData
              });
              const sttData = await sttResponse.json();
              
              // Send transcription to LLM
              const llmResponse = await fetch('http://127.0.0.1:8000/ml/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: sttData.transcription })
              });
              const llmData = await llmResponse.json();
              
              // Get TTS for LLM response
              const ttsResponse = await fetch('http://127.0.0.1:8000/ml/text-to-speech', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: llmData.response })
              });
              
              // Play audio response
              const audioBlob = await ttsResponse.blob();
              const audioUrl = URL.createObjectURL(audioBlob);
              const audio = new Audio(audioUrl);
              
              // Update UI
              document.getElementById('result').innerHTML = `
                <p><strong>You said:</strong> ${sttData.transcription}</p>
                <p><strong>Assistant:</strong> ${llmData.response}</p>
              `;
              
              status.textContent = 'Playing response...';
              audio.onended = () => {
                status.textContent = 'Ready';
                URL.revokeObjectURL(audioUrl);
              };
              audio.play();
              
            } catch (error) {
              console.error('Error:', error);
              status.textContent = 'Error processing request';
            }
          }

          // Initialize recording setup
          setupRecording().catch(error => {
            console.error('Setup error:', error);
            status.textContent = 'Error accessing microphone';
          });
        </script>
      </body>
    </html>
    """
    return html_content