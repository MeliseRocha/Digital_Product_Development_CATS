# Medical Pre-Anamnesis Chatbot

A conversational AI system designed to collect comprehensive medical history data from patients before their appointments. The chatbot streamlines the pre-anamnesis process by gathering essential patient information through structured conversations.

## Overview

This medical chatbot is built using the Rasa framework and deployed on Hetzner infrastructure. It serves as a digital assistant that collects patient medical history data including chronic diseases, medications, allergies, lifestyle factors, and recent medical examinations. The system supports both new patient data collection and returning patient data updates.

## Key Features

- **Intelligent Data Collection**: Gathers comprehensive medical history through conversational flow
- **Patient Authentication**: JWT-based authentication with secure patient identification
- **Conditional Logic**: Adapts questions based on patient responses (e.g., skips pregnancy questions for male patients)
- **File Upload Support**: Allows patients to upload medical exam results and imaging reports
- **Lab Credential Management**: Securely collects imaging lab access credentials for doctor review
- **Data Persistence**: Integrates with backend API for storing and retrieving patient data
- **Update Capability**: Returning patients can review and update existing information

## Core Configuration Files

### domain.yml
The domain file defines the conversational structure and is the **primary configuration file** for the chatbot. It contains:
- **Intents**: User input classifications (greet, affirm, deny, upload_files, etc.)
- **Entities**: Key medical information categories extracted from user messages
- **Slots**: Data storage containers for patient information (chronic_disease, smoking_info, medications, etc.)
- **Forms**: The medical_history_form that orchestrates the complete data collection process
- **Responses**: Predefined chatbot messages and button interfaces for user interaction

### rules.yml
Contains the **conversation flow rules** that govern how the chatbot behaves:
- Form activation and completion logic
- Greeting and authentication workflows
- Data correction and summary presentation rules
- Error handling and fallback behaviors

### nlu.yml
Defines the **Natural Language Understanding** training data:
- Example user phrases for each intent
- Training patterns for entity extraction
- Conversation examples that help the model understand user inputs
- Intent classification examples for medical terminology and responses

## Actions Overview

The `actions.py` file contains custom business logic actions:

### ActionGreetWithJWT
- Authenticates patients using JWT tokens
- Extracts patient ID and gender from authentication
- Initiates the medical history collection process

### ActionCheckPatientData
- Queries existing patient data from the backend
- Determines if patient is new or returning
- Pre-populates forms for returning patients

### ActionSummary
- Presents collected medical information for patient review
- Provides options to modify or confirm data
- Ensures data accuracy before final submission

### ActionSavePatientData
- Persists collected medical history to the backend database
- Handles API communication and error management
- Confirms successful data storage to the patient

### ActionCorrectSlot
- Enables patients to modify specific information fields
- Provides targeted correction workflow
- Maintains data integrity during updates

### ValidateMedicalHistoryForm
- Implements complex form validation logic
- Handles conditional question flows (smoking habits, lab credentials)
- Manages file uploads and credential collection

## Patient Flow

1. **Authentication**: Patient accesses chatbot through secure JWT-enabled link
2. **Data Check**: System verifies if patient has existing medical history
3. **Information Collection**: Guided conversation through medical history topics
4. **File Management**: Upload of medical exam results and imaging reports
5. **Lab Access**: Optional sharing of imaging lab credentials for doctor access
6. **Review & Correction**: Patient reviews all collected information
7. **Final Submission**: Confirmed data is saved to the medical database

## Technical Implementation

- **Framework**: Rasa 3.1
- **Deployment**: Hetzner Cloud Infrastructure
- **Authentication**: JWT token-based patient verification
- **Database Integration**: RESTful API communication
- **File Handling**: Support for medical document uploads
- **Security**: Encrypted credential storage and secure data transmission

## Usage

New patients complete the full medical history questionnaire, while returning patients can review and update their existing information. The system adapts questions based on patient demographics and previous responses, ensuring efficient and personalized data collection.

