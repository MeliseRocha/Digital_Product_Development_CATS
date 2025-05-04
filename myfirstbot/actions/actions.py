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
        return []





class ActionCorrectSlot(Action):
    def name(self) -> Text:
        return "action_correct_slot"

    def run(self, dispatcher, tracker, domain):
        last_user_msg = tracker.latest_message.get("text", "").strip().lower()

        slot_reset_map = {
            "1": "chronic_disease",
            "2": "smoking_info",
            "3": "medicine_info",
            "4": "hospital_info",
            "5": "allergies_info",
            "6": "hereditary_disease",
            "7": "alcohol_info",
            "8": "drug_use",
            "9": "sleep_diet",
            "10": "pregnancy_history",
            "11": "recent_exams",
            "12": "imaging_lab_access",
            "13": "recent_hospitalization"
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
                "I didn't understand which one you'd like to change. Please type the number:\n"
                "1 - Chronic Disease\n"
                "2 - Smoking\n"
                "3 - Medicine Info\n"
                "4 - Hospital Info\n"
                "5 - Allergies\n"
                "6 - Hereditary Diseases\n"
                "7 - Alcohol Info\n"
                "8 - Drug Use\n"
                "9 - Sleep and Diet\n"
                "10 - Pregnancy History\n"
                "11 - Recent Exams\n"
                "12 - Imaging Lab Access\n"
                "13 - Recent Hospitalization Summary"
            ))
            return []
