# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from rasa_sdk.events import ActionExecuted, SessionStarted


class ActionSummary(Action):
    def name(self) -> Text:
        return "action_summary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        chronic = tracker.get_slot("chronic_disease")
        smoking = tracker.get_slot("smoking_info")

        dispatcher.utter_message(text=f"Here's what I've collected:\nChronic Disease: {chronic}\nSmoking Info: {smoking}\nDo you want to change anything? (yes/no)")
        return []

from rasa_sdk.events import SlotSet, ActiveLoop, FollowupAction

from rasa_sdk.events import SlotSet, ActiveLoop, FollowupAction

class ActionCorrectSlot(Action):
    def name(self) -> Text:
        return "action_correct_slot"

    def run(self, dispatcher, tracker, domain):
        last_user_msg = tracker.latest_message.get("text", "").lower()
        print(f"msg: {last_user_msg}")  # For debugging purposes

        # Check if user typed '1' for chronic disease
        if last_user_msg == "1":
            dispatcher.utter_message(text="Please tell me again: Do you have any chronic disease?")
            return [
                SlotSet("chronic_disease", None),
                ActiveLoop("medical_history_form"),
                FollowupAction("medical_history_form")
            ]
        # Check if user typed '2' for smoking info
        elif last_user_msg == "2":
            dispatcher.utter_message(text="Please tell me again: Do you smoke? If yes, how many cigarettes a day?")
            return [
                SlotSet("smoking_info", None),
                ActiveLoop("medical_history_form"),
                FollowupAction("medical_history_form")
            ]
        else:
            dispatcher.utter_message(text="I didn't understand which one you'd like to change. Please type '1' for chronic disease or '2' for smoking.")
            return []
