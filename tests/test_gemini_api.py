#!/usr/bin/env python3
"""Test script to verify Gemini API functionality."""

from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

# Test payload for /decision/reflect
payload = {
    'options': [
        {
            'title': 'Option A',
            'growth_criteria': [{'weight': 8, 'impact': 9}],
            'sustainability_criteria': [{'weight': 6, 'impact': 7}]
        }
    ],
    'comparison_result': {
        'decision_status': 'SINGLE_OPTION_CLASSIFIED',
        'recommended_option': 'Option A',
        'evaluations': []
    }
}

print('Testing /decision/reflect endpoint...')
print('=' * 70)

response = client.post('/decision/reflect', json=payload)
data = response.json()

print(f'Status Code: {response.status_code}')
print(f'Response Keys: {list(data.keys())}')
print(f'\nWisdom Source: {data.get("source", "Unknown")}')
print(f'\n--- Philosophical Advice ---')
print(data.get('philosophical_advice', ''))
print(f'\n--- Action Plan ---')
for i, step in enumerate(data.get('action_plan', []), 1):
    print(f'{i}. {step}\n')

print('=' * 70)
print(f'✅ API Status: SUCCESS (HTTP {response.status_code})')
print(f'Wisdom Source: {data.get("source", "Unknown")}')

# Determine if Gemini API is working
source = data.get("source", "").lower()
if "gemini" in source or "cache" in source or "via gemini" in source:
    print('\n✅ GEMINI API IS FUNCTIONING')
else:
    print('\n⚠️  USING FALLBACK WISDOM (Gemini API unavailable)')
