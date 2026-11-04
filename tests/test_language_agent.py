from app.agents.language_agent import detect_language

test_messages = [
    "My refrigerator does not get cold.",
    "Mon réfrigérateur ne refroidit pas.",
    "الثلاجة لا تبرد."
]

for message in test_messages:

    result = detect_language([
        {
            "role": "user",
            "content": message
        }
    ])

    print("\nMessage:", message)
    print("Detected language:", result)