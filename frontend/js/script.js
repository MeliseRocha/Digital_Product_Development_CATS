let patients = [
    {
      name: "Melise",
      age: 21,
      gender: "Female",
      data: {
        chiefComplaint: "Headache",
        currentSymptoms: "Mild headache, fatigue",
        medications: "Paracetamol",
        smoke: "No",
        alcohol: "No",
        allergies: "Peanuts",
        familyHistory: "Heart disease",
        pastMedicalHistory: "None",
        immunizations: "Up to date",
        recentLabResults: "CBC normal"
      }
    },
    {
      name: "Lucas",
      age: 38,
      gender: "Male",
      data: {
        chiefComplaint: "Cough",
        currentSymptoms: "Dry cough, sore throat",
        medications: "None",
        smoke: "Yes, 10/day",
        alcohol: "Occasionally",
        allergies: "None",
        familyHistory: "Diabetes",
        pastMedicalHistory: "Appendectomy (2015)",
        immunizations: "Up to date",
        recentLabResults: "Chest X-ray clear"
      }
    },
    {
      name: "Alice Johnson",
      age: 42,
      gender: "Female",
      data: {
        chiefComplaint: "High blood pressure",
        currentSymptoms: "No symptoms",
        medications: "Lisinopril",
        smoke: "No",
        alcohol: "Rarely",
        allergies: "Penicillin",
        familyHistory: "Hypertension (father)",
        pastMedicalHistory: "Migraine",
        immunizations: "Up to date",
        recentLabResults: "BP: 145/90 mmHg"
      }
    },
    {
      name: "Brian Smith",
      age: 54,
      gender: "Male",
      data: {
        chiefComplaint: "Routine checkup",
        currentSymptoms: "None",
        medications: "Metformin, Atorvastatin",
        smoke: "Former smoker",
        alcohol: "Yes, weekends",
        allergies: "None",
        familyHistory: "Heart Disease (mother)",
        pastMedicalHistory: "Type 2 Diabetes",
        immunizations: "Flu, COVID-19",
        recentLabResults: "HbA1c: 7.2%"
      }
    },
    {
      name: "Carla Gomez",
      age: 31,
      gender: "Female",
      data: {
        chiefComplaint: "Asthma follow-up",
        currentSymptoms: "Occasional wheezing",
        medications: "Albuterol",
        smoke: "No",
        alcohol: "No",
        allergies: "Peanuts",
        familyHistory: "Asthma (sister)",
        pastMedicalHistory: "Asthma since childhood",
        immunizations: "Up to date",
        recentLabResults: "Spirometry: Mild obstruction"
      }
    },
    {
      name: "David Lee",
      age: 60,
      gender: "Male",
      data: {
        chiefComplaint: "Chest pain",
        currentSymptoms: "Mild chest pain on exertion",
        medications: "Amlodipine",
        smoke: "No",
        alcohol: "Occasionally",
        allergies: "Sulfa drugs",
        familyHistory: "Hypertension (father)",
        pastMedicalHistory: "Coronary artery disease",
        immunizations: "Up to date",
        recentLabResults: "ECG: Normal"
      }
    }
  ];
  
  const patientList = document.getElementById('patientList');
  const patientInfo = document.getElementById('patientInfo');
  
  function renderList(list = patients) {
    patientList.innerHTML = '';
    list.forEach((patient) => {
      const li = document.createElement('li');
      li.textContent = patient.name;
      li.onclick = () => showPatient(patient);
      patientList.appendChild(li);
    });
  }
  
  document.getElementById('searchInput').addEventListener('input', function (e) {
    const query = e.target.value.toLowerCase();
    const filtered = patients.filter(
      patient => patient.name.toLowerCase().includes(query)
    );
    renderList(filtered);
  });
  
  function showPatient(patient) {
    const index = patients.indexOf(patient);
  
    patientInfo.innerHTML = `
      <div style="display: flex; align-items: center; gap: 10px;">
        <h3 style="margin: 0;">${patient.name}</h3>
        <button onclick="editPatient(${index})" class="edit-btn-inline">✏️ Edit</button>
        <button onclick="downloadPDF(${index})" class="pdf-btn-inline">📄 Download PDF</button>
      </div>
      <p><strong>Age:</strong> ${patient.age}</p>
      <p><strong>Gender:</strong> ${patient.gender}</p>
      <p style="font-size: 12px; color: gray;">Last updated: ${patient.updatedAt || 'N/A'}</p>
      <h4>Anamnesis</h4>
      <ul style="list-style-type:none; padding-left:0;">
        <li><strong>Chief Complaint:</strong> ${patient.data.chiefComplaint}</li>
        <li><strong>Current Symptoms:</strong> ${patient.data.currentSymptoms}</li>
        <li><strong>Medications:</strong> ${patient.data.medications}</li>
        <li><strong>Smoke:</strong> ${patient.data.smoke}</li>
        <li><strong>Alcohol:</strong> ${patient.data.alcohol}</li>
        <li><strong>Allergies:</strong> ${patient.data.allergies}</li>
        <li><strong>Family History:</strong> ${patient.data.familyHistory}</li>
        <li><strong>Past Medical History:</strong> ${patient.data.pastMedicalHistory}</li>
        <li><strong>Immunizations:</strong> ${patient.data.immunizations}</li>
        <li><strong>Recent Lab Results:</strong> ${patient.data.recentLabResults}</li>
      </ul>
    `;
  }
  
  function editPatient(index) {
    const p = patients[index];
    modal.classList.remove('hidden');
    form.name.value = p.name;
    form.age.value = p.age;
    form.gender.value = p.gender;
    form.medications.value = p.data.medications;
    form.smoke.value = p.data.smoke;
    form.allergies.value = p.data.allergies;
    form.family.value = p.data.familyHistory;
  
    form.onsubmit = (e) => {
      e.preventDefault();
      const updated = {
        name: form.name.value,
        age: form.age.value,
        gender: form.gender.value,
        updatedAt: new Date().toLocaleString(),
        data: {
          medications: form.medications.value,
          smoke: form.smoke.value,
          allergies: form.allergies.value,
          familyHistory: form.family.value
        }
      };
      patients[index] = updated;
      modal.classList.add('hidden');
      form.reset();
      renderList();
      showPatient(updated, index);
    };
  }
  
  function downloadPDF(index) {
    const { jsPDF } = window.jspdf;
    const patient = patients[index];
    const doc = new jsPDF();
  
    doc.setFontSize(16);
    doc.text(`Patient: ${patient.name}`, 10, 20);
    doc.setFontSize(12);
    doc.text(`Age: ${patient.age}`, 10, 30);
    doc.text(`Gender: ${patient.gender}`, 10, 40);
    doc.text(`Last Updated: ${patient.updatedAt || 'N/A'}`, 10, 50);
  
    let y = 60;
    for (const [key, value] of Object.entries(patient.data)) {
      doc.text(`${key.charAt(0).toUpperCase() + key.slice(1)}: ${value}`, 10, y);
      y += 10;
    }
  
    doc.save(`${patient.name}_record.pdf`);
  }
  
  renderList();
  
  // Right-click ➕ fallback to prompt
  document.querySelector('.add-button').addEventListener('contextmenu', (e) => {
    e.preventDefault();
    const name = prompt("Enter new patient's name:");
    if (!name) return;
    const newPatient = {
      name,
      age: 0,
      gender: "Unknown",
      data: {
        medications: "-",
        smoke: "-",
        allergies: "-",
        familyHistory: "-"
      }
    };
    patients.push(newPatient);
    
    renderList();
  });
  
  // Modal logic
  const modal = document.getElementById('modal');
  const form = document.getElementById('modalForm');
  document.querySelector('.add-button').addEventListener('click', () => {
    modal.classList.remove('hidden');
  });
  document.getElementById('cancel').onclick = () => {
    modal.classList.add('hidden');
    form.reset();
  };
  
  form.onsubmit = (e) => {
    e.preventDefault();
    const patient = {
      name: form.name.value,
      age: form.age.value,
      gender: form.gender.value,
      data: {
        medications: form.medications.value,
        smoke: form.smoke.value,
        allergies: form.allergies.value,
        familyHistory: form.family.value
      }
    };
    const timestamp = new Date().toLocaleString();
    patient.updatedAt = timestamp; // <-- Add timestamp here
    patients.push(patient);
    renderList();
    modal.classList.add('hidden');
    form.reset();
  };
  