const fakePatients = [
    { id: 1, name: "Giamedes, Paul", date: "Mar 14, 2024", status: "processing" },
    { id: 2, name: "Johnson, Emily", date: "Mar 14, 2024", status: "review" },
    { id: 3, name: "Patel, Jamal", date: "Mar 13, 2024", status: "done" },
    { id: 4, name: "Ramirez, Maria", date: "Mar 12, 2024", status: "done" },
  ];
  
  export default function PatientTable({ savedNotes, onViewNote }) {
    return (
      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-100 text-gray-600 uppercase text-sm">
            <tr>
              <th className="px-6 py-4">Date</th>
              <th className="px-6 py-4">Patient</th>
              <th className="px-6 py-4">Status</th>
              <th className="px-6 py-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            {fakePatients.map((patient) => (
              <tr key={patient.id} className="border-t">
                <td className="px-6 py-3">{patient.date}</td>
                <td className="px-6 py-3 font-medium">{patient.name}</td>
                <td className="px-6 py-3">
                  {patient.status === "processing" && (
                    <span className="text-sm bg-green-100 text-green-700 px-2 py-1 rounded-full">processing</span>
                  )}
                  {patient.status === "review" && (
                    <span className="text-sm bg-red-100 text-red-600 px-2 py-1 rounded-full">review draft</span>
                  )}
                  {patient.status === "done" && (
                    <span className="text-sm bg-emerald-100 text-emerald-700 px-2 py-1 rounded-full">view note</span>
                  )}
                </td>
                <td className="px-6 py-3">
                <button
                onClick={() => {
                  const patientNotes = savedNotes.filter(n => n.patient === patient.name);
                  if (patientNotes.length === 0) {
                    alert('No notes for this patient yet.');
                  } else {
                    const latestNote = patientNotes[patientNotes.length - 1];
                    onViewNote(latestNote);
                  }
                }}
                className="text-sm text-indigo-600 hover:underline"
              >
                View SOAP note →
              </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }