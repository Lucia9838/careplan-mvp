import json
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import anthropic

# -------------------------------------------------------
# In-memory "database" — just a plain Python dict
# Lives as long as the Django process is running
# -------------------------------------------------------
CARE_PLANS = {}   # { plan_id: { patient_info, care_plan_text } }


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def generate_careplan(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    body = json.loads(request.body)
    patient_name = body.get('patient_name')
    age          = body.get('age')
    conditions   = body.get('conditions')   # e.g. "diabetes, hypertension"
    notes        = body.get('notes')        # any extra notes from the clinician

    # --- Call Anthropic API (sync, user waits) ---
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    prompt = f"""You are a clinical care coordinator. Generate a structured care plan for the following patient.

Patient Name: {patient_name}
Age: {age}
Medical Conditions: {conditions}
Additional Notes: {notes}

Please produce a care plan with these sections:
1. Summary
2. Goals (short-term and long-term)
3. Interventions
4. Medications (if relevant)
5. Follow-up Schedule

Be concise and clinically appropriate."""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    care_plan_text = message.content[0].text

    # --- Save to in-memory dict ---
    plan_id = str(uuid.uuid4())
    CARE_PLANS[plan_id] = {
        'patient_name': patient_name,
        'age': age,
        'conditions': conditions,
        'notes': notes,
        'care_plan': care_plan_text,
    }

    return JsonResponse({
        'plan_id': plan_id,
        'care_plan': care_plan_text,
    })
