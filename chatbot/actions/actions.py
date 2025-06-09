from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import SlotSet, ActiveLoop, FollowupAction
import psycopg2

from dotenv import load_dotenv
import os
import requests
from typing import Dict, Any
load_dotenv(dotenv_path="./database.env") 

DB_NAME = os.getenv("DB_NAME")  
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")




#def get_connection():
    #return psycopg2.connect(DATABASE_URL)

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

        # Send each line as a separate message
        dispatcher.utter_message(text="Here's what I've collected so far:")

        dispatcher.utter_message(text=f"Chronic Disease: {chronic}")
        dispatcher.utter_message(text=f"Smoking Info: {smoking}")
        dispatcher.utter_message(text=f"Medicine Info: {medicine}")
        dispatcher.utter_message(text=f"Hospital Info: {hospital}")
        dispatcher.utter_message(text=f"Allergies Info: {allergies}")
        dispatcher.utter_message(text=f"Hereditary Diseases: {hereditary}")
        dispatcher.utter_message(text=f"Alcohol Info: {alcohol}")
        dispatcher.utter_message(text=f"Drug Use: {drug_use}")
        dispatcher.utter_message(text=f"Sleep and Diet: {sleep_diet}")
        dispatcher.utter_message(text=f"Pregnancy History: {pregnancy}")
        dispatcher.utter_message(text=f"Recent Exams: {exams}")
        dispatcher.utter_message(text=f"Imaging Lab Access: {lab_access}")
        dispatcher.utter_message(text=f"Recent Hospitalization Summary: {recent_hosp}")

        # Then send the question with buttons
        dispatcher.utter_message(
            text="Do you want to change anything?",
            buttons=[
                {"title": "Yes", "payload": "/affirm"},
                {"title": "No", "payload": "/deny"}
            ]
        )

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
        # TODO add the token in the pot requests
        url = f"https://redcore-latest.onrender.com/patients/{patient_id}/pre-anamnesis"

        payload = {
            "chronic_disease": data.get("chronic_disease"),
            "smoking": data.get("smoking"),
            "medicines": data.get("medicines"),
            "allergies": data.get("allergies"),
            "existing_illness": data.get("existing_illness"),
            "alcohol_drug_use": data.get("alcohol_drug_use"),
            "sleep_diet": data.get("sleep_diet"),
            "pregnancy_history": data.get("pregnancy_history"),
            "recent_exams": data.get("recent_exams"), 
            "recent_hospitalization": data.get("recent_hospitalization")
        }

        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200 or response.status_code == 201:
                print("Data successfully sent to API.")
            else:
                print(f"Failed to send data. Status code: {response.status_code}, Response: {response.text}")

        except requests.RequestException as e:
            print(f"Error during POST request: {e}")


from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ActiveLoop, FollowupAction
from typing import Text, List, Dict, Any

class ActionCorrectSlot(Action):
    def name(self) -> Text:
        return "action_correct_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

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
            buttons = []
            for slot_name in slot_reset_map.keys():
                buttons.append(
                    {
                        "title": slot_name.replace("_", " ").capitalize(),
                        "payload": slot_name
                    }
                )

            dispatcher.utter_message(
                text="Which field would you like to correct? Please choose one of the options below:",
                buttons=buttons
            )
            return []



from rasa_sdk.events import SlotSet, FollowupAction
import sqlite3  # or any DB you're using

class ActionCheckPatientData(Action):
    def name(self) -> Text:
        return "action_check_patient_data"

    def run(self, dispatcher, tracker, domain):
        patient_id = tracker.get_slot("patient_id")

        if not patient_id:
            dispatcher.utter_message(text="Please provide a valid patient ID.")
            return []

        url = f"https://redcore-latest.onrender.com/patients/{patient_id}/pre-anamnesis"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

                if not data:
                    dispatcher.utter_message(text="No existing record found. Let's fill out the medical history.")
                    return [SlotSet("patient_id", patient_id), FollowupAction("medical_history_form")]

                # Map the JSON keys to your slot names
                slot_mapping = {
                    "chronic_disease": data.get("chronic_disease"),
                    "smoking_info": data.get("smoking"),
                    "medicine_info": data.get("medicines"),
                    "allergies_info": data.get("allergies"),
                    "hereditary_disease": data.get("existing_illness"),
                    "alcohol_info": data.get("alcohol_drug_use"),
                    "sleep_diet": data.get("sleep_diet"),
                    "pregnancy_history": data.get("pregnancy_history"),
                    "recent_exams": data.get("recent_exams"),
                    # TODO add imaging lab access to database
                    "imaging_lab_access": None,
                    "recent_hospitalization": data.get("recent_hospitalization"),
                }

                slot_sets = [SlotSet(key, value) for key, value in slot_mapping.items()]
                slot_sets.append(SlotSet("patient_id", patient_id))

                dispatcher.utter_message(text="I found your existing medical history.")
                return slot_sets + [FollowupAction("action_summary")]

            else:
                dispatcher.utter_message(text="No existing record found. Let's fill out the medical history.")
                return [SlotSet("patient_id", patient_id), FollowupAction("medical_history_form")]

        except requests.RequestException as e:
            dispatcher.utter_message(text="Sorry, there was an error accessing your medical history. Please try again later.")
            return []
