export default function ViewNoteModal({ note, onClose }) {
    if (!note) return null;
  
    return (
      <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
        <div className="bg-white max-w-xl w-full p-6 rounded-xl shadow-lg relative">
          <h2 className="text-lg font-bold mb-2">SOAP Note</h2>
          <p className="text-sm text-gray-500 mb-4">
            📅 {note.timestamp} | 👤 {note.patient}
          </p>
  
          {note.content.startsWith('Voice Note:') ? (
            <audio controls src={note.content.replace('Voice Note: ', '')} className="w-full" />
          ) : (
            <pre className="whitespace-pre-wrap text-sm text-gray-800">{note.content}</pre>
          )}
  
          <div className="flex justify-end mt-4">
            <button
              onClick={onClose}
              className="text-sm text-gray-500 hover:text-gray-700"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    );
  }