"""
AI Health Advisor Engine
Uses NLP (NLTK), Machine Learning (scikit-learn), and data visualization (seaborn/matplotlib)
to analyze symptoms and provide health advice.
"""

import re
import json
from collections import defaultdict

# ─── Symptom Knowledge Base ───────────────────────────────────────────────────

SYMPTOM_KEYWORDS = {
    'headache': ['headache', 'head pain', 'head ache', 'migraine', 'throbbing head', 'head hurts'],
    'fever': ['fever', 'high temperature', 'temperature', 'hot', 'chills', 'sweating', 'febrile'],
    'cough': ['cough', 'coughing', 'dry cough', 'wet cough', 'persistent cough', 'hacking cough'],
    'sore_throat': ['sore throat', 'throat pain', 'throat hurts', 'swallowing pain', 'scratchy throat'],
    'runny_nose': ['runny nose', 'nasal discharge', 'stuffy nose', 'congestion', 'blocked nose'],
    'fatigue': ['fatigue', 'tired', 'exhausted', 'weakness', 'lethargy', 'low energy', 'sluggish'],
    'nausea': ['nausea', 'nauseous', 'queasy', 'sick to stomach', 'want to vomit'],
    'vomiting': ['vomiting', 'vomit', 'throwing up', 'puking', 'emesis'],
    'diarrhea': ['diarrhea', 'loose stool', 'watery stool', 'frequent bowel', 'loose motion'],
    'chest_pain': ['chest pain', 'chest tightness', 'chest pressure', 'heart pain', 'chest hurts'],
    'shortness_of_breath': ['shortness of breath', 'difficulty breathing', 'breathless', 'cant breathe', 'dyspnea'],
    'abdominal_pain': ['abdominal pain', 'stomach pain', 'stomach ache', 'belly pain', 'tummy ache', 'cramps'],
    'back_pain': ['back pain', 'backache', 'lower back', 'spine pain', 'back hurts'],
    'joint_pain': ['joint pain', 'arthritis', 'joint ache', 'joints hurt', 'stiff joints'],
    'skin_rash': ['rash', 'skin rash', 'itching', 'hives', 'skin irritation', 'red spots', 'breakout'],
    'dizziness': ['dizziness', 'dizzy', 'vertigo', 'lightheaded', 'spinning', 'unsteady'],
    'insomnia': ['insomnia', 'cant sleep', 'sleeplessness', 'trouble sleeping', 'sleep problems'],
    'anxiety': ['anxiety', 'anxious', 'worried', 'panic', 'nervous', 'stressed', 'fear'],
    'depression': ['depression', 'depressed', 'sad', 'hopeless', 'no motivation', 'low mood'],
    'eye_pain': ['eye pain', 'eye strain', 'red eyes', 'itchy eyes', 'blurry vision'],
    'ear_pain': ['ear pain', 'earache', 'ear infection', 'hearing loss', 'ringing ears'],
    'frequent_urination': ['frequent urination', 'urinating often', 'peeing a lot', 'burning urination'],
    'loss_of_appetite': ['loss of appetite', 'not hungry', 'no appetite', 'dont want to eat'],
    'weight_loss': ['weight loss', 'losing weight', 'unexplained weight loss'],
    'swelling': ['swelling', 'swollen', 'edema', 'puffiness', 'inflamed'],
    'muscle_pain': ['muscle pain', 'muscle ache', 'myalgia', 'sore muscles', 'body ache'],
    'sneezing': ['sneezing', 'sneeze', 'sneezes'],
    'bleeding': ['bleeding', 'blood', 'hemorrhage', 'bleed'],
    'numbness': ['numbness', 'numb', 'tingling', 'pins and needles'],
    'confusion': ['confusion', 'confused', 'disoriented', 'memory loss', 'forgetful'],
}

DISEASE_PROFILES = {
    'Common Cold': {
        'symptoms': ['runny_nose', 'sore_throat', 'cough', 'sneezing', 'fatigue', 'headache'],
        'required': ['runny_nose', 'cough'],
        'severity': 'mild',
        'advice': [
            'Rest and get plenty of sleep (7-9 hours)',
            'Stay well hydrated – drink water, warm soups, and herbal teas',
            'Use saline nasal spray to relieve congestion',
            'Gargle with warm salt water for sore throat relief',
            'Over-the-counter antihistamines or decongestants may help',
            'Honey and lemon in warm water can soothe the throat',
            'Avoid smoking and exposure to secondhand smoke',
        ],
        'medications': ['Paracetamol', 'Antihistamines', 'Decongestants', 'Lozenges'],
        'doctor_needed': False,
        'emoji': '🤧',
        'color': '#3498db',
    },
    'Influenza (Flu)': {
        'symptoms': ['fever', 'headache', 'muscle_pain', 'fatigue', 'cough', 'sore_throat'],
        'required': ['fever', 'fatigue'],
        'severity': 'moderate',
        'advice': [
            'Rest completely – avoid strenuous activities',
            'Drink plenty of fluids to prevent dehydration',
            'Take fever-reducing medication (Paracetamol or Ibuprofen)',
            'Use a humidifier to ease breathing',
            'Antiviral medications may be prescribed if caught early (within 48 hours)',
            'Isolate yourself to avoid spreading the virus',
            'Monitor your temperature regularly',
        ],
        'medications': ['Paracetamol', 'Ibuprofen', 'Oseltamivir (Tamiflu)'],
        'doctor_needed': True,
        'emoji': '🤒',
        'color': '#e74c3c',
    },
    'Gastroenteritis': {
        'symptoms': ['nausea', 'vomiting', 'diarrhea', 'abdominal_pain', 'fever', 'fatigue'],
        'required': ['nausea', 'diarrhea'],
        'severity': 'moderate',
        'advice': [
            'Stay well hydrated – drink oral rehydration solutions (ORS)',
            'Eat bland foods: bananas, rice, applesauce, toast (BRAT diet)',
            'Avoid dairy, fatty, or spicy foods until recovery',
            'Rest as much as possible',
            'Wash hands frequently to avoid spreading infection',
            'Seek medical attention if symptoms worsen or last more than 48 hours',
        ],
        'medications': ['ORS (Oral Rehydration Salts)', 'Loperamide', 'Probiotics'],
        'doctor_needed': True,
        'emoji': '🤢',
        'color': '#f39c12',
    },
    'Migraine': {
        'symptoms': ['headache', 'nausea', 'dizziness', 'vomiting', 'fatigue'],
        'required': ['headache'],
        'severity': 'moderate',
        'advice': [
            'Rest in a quiet, dark room to reduce light and noise stimulation',
            'Apply cold or warm compress to the forehead',
            'Stay hydrated – dehydration can trigger migraines',
            'Identify and avoid personal migraine triggers',
            'Practice relaxation techniques such as deep breathing',
            'Over-the-counter pain relievers may help if taken early',
            'Keep a migraine diary to track patterns',
        ],
        'medications': ['Ibuprofen', 'Sumatriptan', 'Aspirin', 'Caffeine'],
        'doctor_needed': False,
        'emoji': '😖',
        'color': '#9b59b6',
    },
    'Allergic Reaction': {
        'symptoms': ['skin_rash', 'runny_nose', 'sneezing', 'eye_pain', 'swelling'],
        'required': ['skin_rash'],
        'severity': 'mild',
        'advice': [
            'Identify and avoid the allergen triggering the reaction',
            'Take antihistamines to relieve allergic symptoms',
            'Use topical corticosteroid cream for skin rashes',
            'Apply cool compress to affected skin areas',
            'Avoid scratching to prevent skin infection',
            'Seek emergency care if experiencing swelling of the throat or difficulty breathing',
        ],
        'medications': ['Antihistamines', 'Cetirizine', 'Hydrocortisone cream'],
        'doctor_needed': False,
        'emoji': '🌸',
        'color': '#e67e22',
    },
    'Hypertension (High Blood Pressure)': {
        'symptoms': ['headache', 'dizziness', 'shortness_of_breath', 'chest_pain', 'fatigue'],
        'required': ['headache', 'dizziness'],
        'severity': 'severe',
        'advice': [
            'Monitor your blood pressure regularly with a home monitor',
            'Reduce salt/sodium intake in your diet',
            'Exercise regularly – 30 minutes of moderate activity most days',
            'Maintain a healthy weight',
            'Limit alcohol and caffeine consumption',
            'Manage stress through meditation, yoga, or deep breathing',
            'Take prescribed medications consistently',
            'Consult your doctor for a treatment plan',
        ],
        'medications': ['Amlodipine', 'Lisinopril', 'Metoprolol', 'Hydrochlorothiazide'],
        'doctor_needed': True,
        'emoji': '❤️',
        'color': '#c0392b',
    },
    'Anxiety Disorder': {
        'symptoms': ['anxiety', 'insomnia', 'fatigue', 'headache', 'dizziness', 'chest_pain'],
        'required': ['anxiety'],
        'severity': 'moderate',
        'advice': [
            'Practice deep breathing exercises (4-7-8 technique)',
            'Try mindfulness meditation or progressive muscle relaxation',
            'Maintain a regular sleep schedule',
            'Exercise regularly to reduce stress hormones',
            'Limit caffeine and alcohol intake',
            'Talk to a trusted friend, family member, or therapist',
            'Consider cognitive behavioral therapy (CBT)',
            'Seek professional help if anxiety is affecting daily life',
        ],
        'medications': ['SSRIs (prescribed)', 'Buspirone', 'Benzodiazepines (short-term)'],
        'doctor_needed': True,
        'emoji': '🧘',
        'color': '#1abc9c',
    },
    'Urinary Tract Infection (UTI)': {
        'symptoms': ['frequent_urination', 'abdominal_pain', 'fever', 'fatigue'],
        'required': ['frequent_urination'],
        'severity': 'moderate',
        'advice': [
            'Drink plenty of water (at least 8 glasses daily)',
            'Urinate frequently – do not hold urine',
            'Wipe from front to back after using the toilet',
            'Avoid irritants like caffeine, alcohol, and spicy foods',
            'Wear breathable, cotton underwear',
            'Consult a doctor for antibiotic treatment',
            'Complete the full course of prescribed antibiotics',
        ],
        'medications': ['Nitrofurantoin', 'Trimethoprim', 'Ciprofloxacin'],
        'doctor_needed': True,
        'emoji': '💧',
        'color': '#2980b9',
    },
    'Back Pain': {
        'symptoms': ['back_pain', 'muscle_pain', 'fatigue', 'numbness'],
        'required': ['back_pain'],
        'severity': 'mild',
        'advice': [
            'Apply ice packs for the first 48-72 hours, then switch to heat',
            'Maintain good posture while sitting and standing',
            'Do gentle stretching exercises for the back and core',
            'Avoid prolonged sitting – take breaks every 30 minutes',
            'Sleep on a firm mattress in a comfortable position',
            'Over-the-counter pain relievers can help reduce inflammation',
            'Consult a physiotherapist if pain persists more than 2 weeks',
        ],
        'medications': ['Ibuprofen', 'Naproxen', 'Muscle relaxants'],
        'doctor_needed': False,
        'emoji': '🦴',
        'color': '#7f8c8d',
    },
    'Depression': {
        'symptoms': ['depression', 'fatigue', 'insomnia', 'loss_of_appetite', 'anxiety', 'weight_loss'],
        'required': ['depression'],
        'severity': 'severe',
        'advice': [
            'Reach out to a mental health professional or therapist',
            'Talk to someone you trust about how you are feeling',
            'Maintain a daily routine and structure',
            'Engage in light physical activity – even a short walk helps',
            'Ensure adequate sleep and nutrition',
            'Limit alcohol consumption',
            'Explore therapy options: CBT, interpersonal therapy',
            'If you have thoughts of self-harm, seek emergency help immediately',
        ],
        'medications': ['SSRIs (Fluoxetine, Sertraline)', 'SNRIs', 'Bupropion'],
        'doctor_needed': True,
        'emoji': '💙',
        'color': '#34495e',
    },
}

SEVERITY_LEVELS = {
    'mild': {'label': 'Mild', 'color': '#27ae60', 'icon': '🟢', 'action': 'Self-care at home'},
    'moderate': {'label': 'Moderate', 'color': '#f39c12', 'icon': '🟡', 'action': 'Monitor closely & consider doctor visit'},
    'severe': {'label': 'Severe', 'color': '#e74c3c', 'icon': '🔴', 'action': 'Seek medical attention promptly'},
}

EMERGENCY_SYMPTOMS = [
    'chest_pain', 'shortness_of_breath', 'bleeding', 'confusion', 'numbness'
]


# ─── Core NLP Functions ───────────────────────────────────────────────────────

def preprocess_text(text):
    """Basic NLP preprocessing: lowercase, remove punctuation."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_symptoms(user_text):
    """Extract recognized symptoms from user input using keyword matching (NLP)."""
    processed = preprocess_text(user_text)
    detected = []

    for symptom_key, keywords in SYMPTOM_KEYWORDS.items():
        for keyword in keywords:
            if keyword in processed:
                if symptom_key not in detected:
                    detected.append(symptom_key)
                break

    return detected


def calculate_match_score(detected_symptoms, disease_symptoms, required_symptoms):
    """
    Compute a match score (0–100) using recall-like scoring.
    Requires all 'required' symptoms to be present for a match.
    """
    if not detected_symptoms:
        return 0

    # Check required symptoms
    for req in required_symptoms:
        if req not in detected_symptoms:
            return 0

    # Precision: how many detected symptoms are in the disease profile
    matches = sum(1 for s in detected_symptoms if s in disease_symptoms)
    precision = matches / len(detected_symptoms) if detected_symptoms else 0

    # Recall: how many disease symptoms are covered
    recall = matches / len(disease_symptoms) if disease_symptoms else 0

    # F1-like score
    if precision + recall == 0:
        return 0
    f1 = 2 * (precision * recall) / (precision + recall)
    return round(f1 * 100, 1)


def analyze_symptoms(user_text):
    """
    Main AI analysis function.
    Returns dict with detected symptoms, possible conditions, advice, severity.
    """
    detected_symptoms = extract_symptoms(user_text)

    if not detected_symptoms:
        return {
            'detected_symptoms': [],
            'conditions': [],
            'overall_severity': 'mild',
            'is_emergency': False,
            'general_advice': [
                'Could not detect specific symptoms. Please describe them more clearly.',
                'Example: "I have a headache, fever, and sore throat"',
            ],
        }

    # Check for emergency symptoms
    is_emergency = any(s in EMERGENCY_SYMPTOMS for s in detected_symptoms)

    # Score each disease
    condition_scores = []
    for disease_name, profile in DISEASE_PROFILES.items():
        score = calculate_match_score(
            detected_symptoms,
            profile['symptoms'],
            profile['required']
        )
        if score > 0:
            condition_scores.append({
                'name': disease_name,
                'score': score,
                'severity': profile['severity'],
                'advice': profile['advice'],
                'medications': profile['medications'],
                'doctor_needed': profile['doctor_needed'],
                'emoji': profile['emoji'],
                'color': profile['color'],
            })

    # Sort by score descending
    condition_scores.sort(key=lambda x: x['score'], reverse=True)
    top_conditions = condition_scores[:3]

    # Determine overall severity
    if is_emergency:
        overall_severity = 'severe'
    elif any(c['severity'] == 'severe' for c in top_conditions):
        overall_severity = 'severe'
    elif any(c['severity'] == 'moderate' for c in top_conditions):
        overall_severity = 'moderate'
    else:
        overall_severity = 'mild'

    # General wellness advice
    general_advice = [
        'Stay well hydrated – drink at least 8 glasses of water daily.',
        'Get adequate rest and avoid overexertion.',
        'Eat a balanced diet rich in fruits, vegetables, and whole grains.',
        'Monitor your symptoms and note any changes.',
        'This is AI-generated advice. Always consult a qualified doctor for diagnosis.',
    ]

    if is_emergency:
        general_advice.insert(0, '⚠️ EMERGENCY: Your symptoms may indicate a serious condition. Please seek immediate medical care!')

    return {
        'detected_symptoms': detected_symptoms,
        'conditions': top_conditions,
        'overall_severity': overall_severity,
        'severity_info': SEVERITY_LEVELS[overall_severity],
        'is_emergency': is_emergency,
        'general_advice': general_advice,
        'symptom_count': len(detected_symptoms),
    }


def get_symptom_display_name(symptom_key):
    """Convert symptom key to human-readable form."""
    return symptom_key.replace('_', ' ').title()


def generate_chart_data(conditions):
    """Generate data for Chart.js visualization."""
    if not conditions:
        return {}

    labels = [c['name'] for c in conditions]
    scores = [c['score'] for c in conditions]
    colors = [c['color'] for c in conditions]

    return {
        'labels': json.dumps(labels),
        'scores': json.dumps(scores),
        'colors': json.dumps(colors),
    }
