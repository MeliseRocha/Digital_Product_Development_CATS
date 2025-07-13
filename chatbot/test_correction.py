#!/usr/bin/env python3
"""
Test script to simulate the correction action and see what happens
This helps us debug the correction flow without needing a full Rasa setup
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'actions'))

from actions.actions import ActionCorrectSlot
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class MockTracker:
    def __init__(self, slots=None, latest_message=None):
        self.slots = slots or {}
        self.latest_message = latest_message or {}
    
    def get_slot(self, slot_name):
        return self.slots.get(slot_name)

class MockDispatcher:
    def __init__(self):
        self.messages = []
    
    def utter_message(self, text=None, buttons=None, **kwargs):
        message = {"text": text}
        if buttons:
            message["buttons"] = buttons
        self.messages.append(message)
        print(f"🤖 Bot says: {text}")
        if buttons:
            print(f"🔘 Buttons: {[b['title'] for b in buttons]}")

def test_scenario(scenario_name, tracker, expected_behavior):
    print(f"\n{'='*50}")
    print(f"🧪 Testing: {scenario_name}")
    print(f"{'='*50}")
    
    dispatcher = MockDispatcher()
    action = ActionCorrectSlot()
    
    print(f"📥 Input: {tracker.latest_message}")
    print(f"📊 Current slots: {tracker.slots}")
    
    try:
        result = action.run(dispatcher, tracker, {})
        print(f"✅ Action completed successfully")
        print(f"📤 Result events: {result}")
        print(f"💬 Bot messages: {len(dispatcher.messages)} message(s)")
        
        # Check if behavior matches expectations
        if expected_behavior(result, dispatcher.messages):
            print(f"✅ Test PASSED: Behavior matches expectations")
        else:
            print(f"❌ Test FAILED: Unexpected behavior")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("🚀 Testing Correction Action Functionality")
    print("This simulates different button click scenarios")
    
    # Test 1: Button sends slot name directly (working buttons)
    test_scenario(
        "Button sends slot name directly",
        MockTracker(
            slots={"recent_hospitalization": "Yes", "recent_hospitalization_status": True},
            latest_message={
                "text": "recent_hospitalization",
                "intent": {"name": "recent_hospitalization"}
            }
        ),
        lambda result, messages: any("reset" in str(msg).lower() for msg in messages)
    )
    
    # Test 2: Button sends /affirm only (broken buttons)
    test_scenario(
        "Button sends /affirm only (broken buttons)",
        MockTracker(
            slots={"recent_hospitalization": "Yes", "recent_hospitalization_status": True},
            latest_message={
                "text": "/affirm",
                "intent": {"name": "affirm"}
            }
        ),
        lambda result, messages: any("which field" in str(msg).lower() for msg in messages)
    )
    
    # Test 3: Confirmation flow - first step
    test_scenario(
        "User selects field for correction",
        MockTracker(
            slots={"recent_hospitalization": "Yes"},
            latest_message={
                "text": "recent_hospitalization",
                "intent": {"name": "recent_hospitalization"}
            }
        ),
        lambda result, messages: any("do you want to correct" in str(msg).lower() for msg in messages)
    )
    
    # Test 4: Confirmation flow - user confirms
    test_scenario(
        "User confirms correction",
        MockTracker(
            slots={
                "recent_hospitalization": "Yes", 
                "pending_correction_slot": "recent_hospitalization"
            },
            latest_message={
                "text": "/affirm",
                "intent": {"name": "affirm"}
            }
        ),
        lambda result, messages: any("reset" in str(msg).lower() for msg in messages)
    )
    
    # Test 5: Typed field name
    test_scenario(
        "User types field name",
        MockTracker(
            slots={"recent_hospitalization": "Yes"},
            latest_message={
                "text": "Recent Hospitalization",
                "intent": {"name": "inform"}
            }
        ),
        lambda result, messages: any("do you want to correct" in str(msg).lower() for msg in messages)
    )

if __name__ == "__main__":
    main()
