#!/usr/bin/env python3
"""
Simple test to validate our correction logic
This simulates the ActionCorrectSlot logic without requiring Rasa SDK
"""

def test_correction_logic():
    print("🚀 Testing Correction Logic")
    print("="*50)
    
    # Simulate the slot reset map
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
        "recent_hospitalization": "recent_hospitalization",
    }
    
    def test_scenario(name, last_user_msg, button_payload, pending_correction, expected_match):
        print(f"\n🧪 Test: {name}")
        print(f"   Input: '{last_user_msg}', Button: '{button_payload}', Pending: '{pending_correction}'")
        
        # Simulate the matching logic from our ActionCorrectSlot
        matched_slot = None
        
        # If user confirms with /affirm and we have a pending correction
        if button_payload == "affirm" and pending_correction and pending_correction in slot_reset_map:
            matched_slot = pending_correction
            print(f"   ✅ Using pending correction slot: {matched_slot}")
        else:
            # Check if user input matches any slot name
            if last_user_msg in slot_reset_map:
                matched_slot = last_user_msg
                print(f"   ✅ Exact text match found: {matched_slot}")
            elif button_payload and button_payload in slot_reset_map:
                matched_slot = button_payload
                print(f"   ✅ Button payload match found: {matched_slot}")
            else:
                # Try fuzzy matching
                for slot_key in slot_reset_map.keys():
                    human_readable = slot_key.replace("_", " ").lower()
                    title_case = slot_key.replace("_", " ").title().lower()
                    
                    if (human_readable == last_user_msg or 
                        title_case == last_user_msg or
                        slot_key.replace("_", "") == last_user_msg.replace(" ", "")):
                        matched_slot = slot_key
                        print(f"   ✅ Fuzzy match found: {matched_slot}")
                        break
                
                if not matched_slot:
                    print(f"   ❌ No match found")
        
        # Check if result matches expectation
        if matched_slot == expected_match:
            print(f"   ✅ PASS: Got expected result '{matched_slot}'")
        else:
            print(f"   ❌ FAIL: Expected '{expected_match}', got '{matched_slot}'")
        
        return matched_slot == expected_match
    
    # Run test scenarios
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Direct button with slot name
    total_tests += 1
    if test_scenario("Direct button with slot name", 
                    "recent_hospitalization", "recent_hospitalization", None, "recent_hospitalization"):
        tests_passed += 1
    
    # Test 2: Button sends /affirm only
    total_tests += 1
    if test_scenario("Button sends /affirm only", 
                    "/affirm", "affirm", None, None):
        tests_passed += 1
    
    # Test 3: Confirmation with pending correction
    total_tests += 1
    if test_scenario("Confirmation with pending correction", 
                    "/affirm", "affirm", "recent_hospitalization", "recent_hospitalization"):
        tests_passed += 1
    
    # Test 4: Typed human-readable name
    total_tests += 1
    if test_scenario("Typed human-readable name", 
                    "recent hospitalization", "inform", None, "recent_hospitalization"):
        tests_passed += 1
    
    # Test 5: Typed title case
    total_tests += 1
    if test_scenario("Typed title case", 
                    "Recent Hospitalization", "inform", None, "recent_hospitalization"):
        tests_passed += 1
    
    # Test 6: Exact slot name typed
    total_tests += 1
    if test_scenario("Exact slot name typed", 
                    "recent_hospitalization", "inform", None, "recent_hospitalization"):
        tests_passed += 1
    
    print(f"\n{'='*50}")
    print(f"🏁 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ All tests passed! The correction logic should work correctly.")
    else:
        print("❌ Some tests failed. There might be issues with the logic.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    test_correction_logic()
