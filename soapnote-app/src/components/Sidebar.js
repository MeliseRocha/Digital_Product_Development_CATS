export default function Sidebar() {
  return (
    <div className="w-60 h-screen bg-white border-r shadow-lg p-6 flex flex-col justify-between">
      <div>
        <h1 className="text-2xl font-bold mb-8 text-indigo-700">soapnotescribe</h1>

        <nav className="space-y-4 text-gray-700 text-sm font-medium">
          <a href="#" className="block text-indigo-600">SOAP Notes</a>
          <a href="#" className="block hover:text-indigo-600">New Note</a>
          <a href="#" className="block hover:text-indigo-600">Templates</a>
          <a href="#" className="block hover:text-indigo-600">Patients</a>
          <a href="#" className="block hover:text-indigo-600">Settings</a>
        </nav>
      </div>

      <button className="text-sm font-medium text-red-600 hover:underline ml-2 mb-4">log out</button>
    </div>
  );
}