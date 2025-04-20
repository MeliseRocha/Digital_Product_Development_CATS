import { useState } from 'react';
import Sidebar from './components/Sidebar';
import PatientTable from './components/PatientTable';
import AddNoteModal from './components/AddNoteModal';
import ViewNoteModal from './components/ViewNoteModal';

function App() {
  const [showModal, setShowModal] = useState(false);
  const [savedNotes, setSavedNotes] = useState([]);
  const [viewingNote, setViewingNote] = useState(null);

  const handleSaveNote = (content, patientName) => {
    const now = new Date();
    const timestamp = now.toLocaleString('en-US', {
      dateStyle: 'medium',
      timeStyle: 'short'
    });
  
    setSavedNotes([...savedNotes, {
      patient: patientName,
      content,
      timestamp
    }]);
  };

  const handleDeleteNote = (indexToDelete) => {
    setSavedNotes(savedNotes.filter((_, index) => index !== indexToDelete));
  };

  return (
    <div className="flex h-screen">
      <Sidebar />
      <main className="flex-1 bg-gray-50 p-6 relative overflow-auto">
        <h2 className="text-2xl font-semibold mb-6">SOAP Notes</h2>

        <PatientTable savedNotes={savedNotes} onViewNote={setViewingNote} />

        {/* Display saved notes */}
        <div className="mt-10 space-y-4">
        {savedNotes.map((note, idx) => (
        <div key={idx} className="bg-white rounded-lg shadow p-4 relative">
          <div className="text-sm text-gray-500 mb-1">
            📅 {note.timestamp} | 👤 {note.patient}
          </div>

          {note.content.startsWith('Voice Note:') ? (
            <>
              <p className="text-sm font-semibold text-indigo-600 mb-1">🎤 Voice Note</p>
              <audio controls src={note.content.replace('Voice Note: ', '')} className="w-full" />
            </>
          ) : (
            <pre className="whitespace-pre-wrap text-sm text-gray-800">{note.content}</pre>
          )}

          <button
            onClick={() => handleDeleteNote(idx)}
            className="absolute top-2 right-2 text-red-400 hover:text-red-600 text-xs"
          >
            🗑️ Delete
          </button>
        </div>
      ))}
        </div>

        {/* ➕ Floating Button */}
        <button
          onClick={() => setShowModal(true)}
          className="fixed bottom-8 right-8 bg-indigo-600 hover:bg-indigo-700 text-white w-14 h-14 text-3xl rounded-full shadow-lg"
        >
          +
        </button>

        {/* Modal */}
        {showModal && (
          <AddNoteModal
            onClose={() => setShowModal(false)}
            onSave={handleSaveNote}
          />
        )}
        {viewingNote && (
          <ViewNoteModal note={viewingNote} onClose={() => setViewingNote(null)} />
        )}
      </main>
    </div>
  );
}

export default App;