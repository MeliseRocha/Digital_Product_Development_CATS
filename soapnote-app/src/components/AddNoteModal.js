import { useState, useRef } from 'react';
import { MicrophoneIcon, StopIcon, ArrowUpTrayIcon } from '@heroicons/react/24/outline';


export default function AddNoteModal({ onClose, onSave }) {
  const [textPreview, setTextPreview] = useState('');
  const [isReading, setIsReading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const [selectedPatient, setSelectedPatient] = useState('');
  const fakePatients = ["Johnson, Emily", "Patel, Jamal", "Ramirez, Maria", "Giamedes, Paul"];
  const mediaRecorderRef = useRef(null);
  const audioChunks = useRef([]);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file && file.name.endsWith('.txt')) {
      setIsReading(true);
      const reader = new FileReader();
      reader.onload = () => {
        setTextPreview(reader.result);
        setIsReading(false);
      };
      reader.readAsText(file);
    } else {
      alert('Please upload a .txt file');
    }
  };

  const toggleRecording = async () => {
    if (isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    } else {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;
      audioChunks.current = [];

      recorder.ondataavailable = (e) => {
        audioChunks.current.push(e.data);
      };

      recorder.onstop = () => {
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/webm' });
        const url = URL.createObjectURL(audioBlob);
        setAudioURL(url);
      };

      recorder.start();
      setIsRecording(true);
    }
  };

  return (
    
    <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
      <div className="bg-white w-full max-w-lg p-6 rounded-xl shadow-lg relative">
        <h2 className="text-lg font-bold mb-4">Generate SOAP Note</h2>

        <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">Select patient</label>
        <select
          className="block w-full border rounded p-2"
          value={selectedPatient}
          onChange={(e) => setSelectedPatient(e.target.value)}
        >
          <option value="" disabled>Select a patient</option>
          {fakePatients.map((p) => (
            <option key={p} value={p}>{p}</option>
          ))}
        </select>
      </div>
        {/* .txt Upload */}
        <div className="mb-4">
        <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-1">
          <ArrowUpTrayIcon className="w-5 h-5 text-gray-500" />
            Upload .txt file
        </label>
          <input
            type="file"
            accept=".txt"
            onChange={handleFileUpload}
            className="block w-full border rounded p-2"
          />
          {isReading && (
            <p className="mt-2 text-sm text-gray-500 animate-pulse">📄 Reading file...</p>
          )}
          {textPreview && (
            <div className="mt-2 p-3 bg-gray-100 text-sm rounded h-32 overflow-auto whitespace-pre-wrap">
              {textPreview}
            </div>
          )}
        </div>

        {/* Mic Recording */}
        <div className="mb-4">
          <button
            onClick={toggleRecording}
            className={`w-full py-2 px-4 rounded text-white font-semibold flex items-center justify-center gap-2 ${
              isRecording ? 'bg-red-600 hover:bg-red-700' : 'bg-indigo-600 hover:bg-indigo-700'
            }`}
          >
            {isRecording ? <StopIcon className="w-5 h-5" /> : <MicrophoneIcon className="w-5 h-5" />}
            {isRecording ? 'Stop Recording' : 'Start Recording'}
            {isRecording && <span className="animate-ping ml-2 h-2 w-2 rounded-full bg-white opacity-75"></span>}
          </button>

          {audioURL && (
            <audio className="mt-3 w-full" controls src={audioURL}></audio>
          )}
        </div>

        {/* Footer */}
      

        <div className="flex justify-end gap-4 mt-4">
  <button
    onClick={onClose}
    className="text-sm text-gray-500 hover:text-gray-700"
  >
    Cancel
  </button>
  <button
    onClick={() => {
      if (!selectedPatient) {
        alert("Please select a patient.");
        return;
      }
    
      if (textPreview) {
        onSave(textPreview, selectedPatient);
        onClose();
      } else if (audioURL) {
        onSave(`Voice Note: ${audioURL}`, selectedPatient);
        onClose();
      } else {
        alert("Please upload a .txt file or record audio.");
      }
    }}
    className="bg-indigo-600 text-white px-4 py-2 rounded text-sm hover:bg-indigo-700"
  >
    Save Note
  </button>
</div>
      </div>
    </div>
  );
}