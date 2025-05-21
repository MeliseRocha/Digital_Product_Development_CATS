from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import SlotSet, ActiveLoop, FollowupAction



class ActionSummary(Action):
    def name(self) -> Text:
        return "action_summary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        patient_id = tracker.get_slot("patient_id")
        print(f"patient id {patient_id}")

        chronic = tracker.get_slot("chronic_disease")
        smoking = tracker.get_slot("smoking_info")
        medicine = tracker.get_slot("medicine_info")
        hospital = tracker.get_slot("hospital_info")
        allergies = tracker.get_slot("allergies_info")
        hereditary = tracker.get_slot("hereditary_disease")
        alcohol = tracker.get_slot("alcohol_info")  
        drug_use = tracker.get_slot("drug_use")
        sleep_diet = tracker.get_slot("sleep_diet")
        pregnancy = tracker.get_slot("pregnancy_history")
        exams = tracker.get_slot("recent_exams")
        lab_access = tracker.get_slot("imaging_lab_access")
        recent_hosp = tracker.get_slot("recent_hospitalization")

        summary = (
            f"Here's what I've collected:\n"
            f"Chronic Disease: {chronic}\n"
            f"Smoking Info: {smoking}\n"
            f"Medicine Info: {medicine}\n"
            f"Hospital Info: {hospital}\n"
            f"Allergies Info: {allergies}\n"
            f"Hereditary Diseases: {hereditary}\n"
            f"Alcohol Info: {alcohol}\n"
            f"Drug Use: {drug_use}\n"
            f"Sleep and Diet: {sleep_diet}\n"
            f"Pregnancy History: {pregnancy}\n"
            f"Recent Exams: {exams}\n"
            f"Imaging Lab Access: {lab_access}\n"
            f"Recent Hospitalization Summary: {recent_hosp}\n\n"
            f"Do you want to change anything? (yes/no)"
        )

        dispatcher.utter_message(text=summary)
        return [SlotSet("patient_id", patient_id)]


import sqlite3

class ActionSavePatientData(Action):
    def name(self) -> Text:
        return "action_save_patient_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        patient_id = tracker.get_slot("patient_id")
        print(f"id {patient_id}")

        if not patient_id:
            dispatcher.utter_message("Missing patient ID. Cannot save.")
            return []

        data = {
            "chronic_disease": tracker.get_slot("chronic_disease"),
            "smoking_info": tracker.get_slot("smoking_info"),
            "medicine_info": tracker.get_slot("medicine_info"),
            "hospital_info": tracker.get_slot("hospital_info"),
            "allergies_info": tracker.get_slot("allergies_info"),
            "hereditary_disease": tracker.get_slot("hereditary_disease"),
            "alcohol_info": tracker.get_slot("alcohol_info"),
            "drug_use": tracker.get_slot("drug_use"),
            "sleep_diet": tracker.get_slot("sleep_diet"),
            "pregnancy_history": tracker.get_slot("pregnancy_history"),
            "recent_exams": tracker.get_slot("recent_exams"),
            "imaging_lab_access": tracker.get_slot("imaging_lab_access"),
            "recent_hospitalization": tracker.get_slot("recent_hospitalization")
        }

        self.save_to_database(patient_id, data)
        dispatcher.utter_message("Your medical history has been saved.")
        return []

    def save_to_database(self, patient_id: str, data: Dict[str, Any]):
        conn = sqlite3.connect("/home/melise/Digital_Product_Development_CATS/chatbot/patients.db")
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_history (
                patient_id TEXT PRIMARY KEY,
                chronic_disease TEXT,
                smoking_info TEXT,
                medicine_info TEXT,
                hospital_info TEXT,
                allergies_info TEXT,
                hereditary_disease TEXT,
                alcohol_info TEXT,
                drug_use TEXT,
                sleep_diet TEXT,
                pregnancy_history TEXT,
                recent_exams TEXT,
                imaging_lab_access TEXT,
                recent_hospitalization TEXT
            )
        ''')

        cursor.execute('''
            INSERT OR REPLACE INTO medical_history (
                patient_id, chronic_disease, smoking_info, medicine_info, hospital_info,
                allergies_info, hereditary_disease, alcohol_info, drug_use,
                sleep_diet, pregnancy_history, recent_exams,
                imaging_lab_access, recent_hospitalization
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            patient_id,
            data["chronic_disease"],
            data["smoking_info"],
            data["medicine_info"],
            data["hospital_info"],
            data["allergies_info"],
            data["hereditary_disease"],
            data["alcohol_info"],
            data["drug_use"],
            data["sleep_diet"],
            data["pregnancy_history"],
            data["recent_exams"],
            data["imaging_lab_access"],
            data["recent_hospitalization"]
        ))

        conn.commit()
        conn.close()



class ActionCorrectSlot(Action):
    def name(self) -> Text:
        return "action_correct_slot"

    def run(self, dispatcher, tracker, domain):
        last_user_msg = tracker.latest_message.get("text", "").strip().lower()
        slot_reset_map = {
            "chronic_disease": "chronic_disease",
            "smoking_info": "smoking_info",
            "medicine_info": "medicine_info",
            "hospital_info": "hospital_info",
            "allergies_info": "allergies_info",
            "hereditary_disease": "hereditary_disease",
            "alcohol_info": "alcohol_info",
            "drug_use": "drug_use",
            "sleep_diet": "sleep_diet",
            "pregnancy_history": "pregnancy_history",
            "recent_exams": "recent_exams",
            "imaging_lab_access": "imaging_lab_access",
            "recent_hospitalization": "recent_hospitalization"
        }

        if last_user_msg in slot_reset_map:
            slot_to_reset = slot_reset_map[last_user_msg]
            return [
                SlotSet(slot_to_reset, None),
                ActiveLoop("medical_history_form"),
                FollowupAction("medical_history_form")
            ]
        else:
            dispatcher.utter_message(text=(
                "I didn't understand which one you'd like to change. Please type the exact field name from the list below:\n"
                "- chronic_disease\n"
                "- smoking_info\n"
                "- medicine_info\n"
                "- hospital_info\n"
                "- allergies_info\n"
                "- hereditary_disease\n"
                "- alcohol_info\n"
                "- drug_use\n"
                "- sleep_diet\n"
                "- pregnancy_history\n"
                "- recent_exams\n"
                "- imaging_lab_access\n"
                "- recent_hospitalization"
            ))
            return []

from rasa_sdk.events import SlotSet, FollowupAction
import sqlite3  # or any DB you're using

class ActionCheckPatientData(Action):
    def name(self) -> Text:
        return "action_check_patient_data"

    def run(self, dispatcher, tracker, domain):
        #patient_id = tracker.get_slot("patient_id")

        if not patient_id:
            dispatcher.utter_message(text="Please provide a valid patient ID.")
            return []

        conn = sqlite3.connect("/home/melise/Digital_Product_Development_CATS/chatbot/patients.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM medical_history WHERE patient_id=?", (patient_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            slot_names = [
                "chronic_disease", "smoking_info", "medicine_info", "hospital_info",
                "allergies_info", "hereditary_disease", "alcohol_info", "drug_use",
                "sleep_diet", "pregnancy_history", "recent_exams",
                "imaging_lab_access", "recent_hospitalization"
            ]

            slot_sets = [SlotSet(name, value) for name, value in zip(slot_names, result[1:])]  # skip patient_id
            slot_sets.append(SlotSet("patient_id", patient_id))  # ensure patient_id is always set

            dispatcher.utter_message(text="I found your existing medical history.")
            return slot_sets + [FollowupAction("action_summary")]
        else:
            dispatcher.utter_message(text="No existing record found. Let's fill out the medical history.")
            return [SlotSet("patient_id", patient_id), FollowupAction("medical_history_form")]
