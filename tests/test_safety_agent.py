from app.agents.safety_agent import classify_safety

test_cases = [
    "My refrigerator does not get cold.",
    "I smell something burning near my refrigerator.",
    "My refrigerator is behaving strangely."
]

for message in test_cases:

    conversation = [
        {
            "role": "user",
            "content": message
        }
    ]

    result = classify_safety(conversation)

    print("\nCustomer:", message)
    print("Classification:", result["classification"])
    print("Reason:", result["reason"])