from app.agents.information_agent import extract_information

conversation = [
    {
        "role": "user",
        "content": "My refrigerator smells like something is burning. Its model is GTV-450."
    }
]

result = extract_information(conversation)

print("\nAGENT 1 RESULT:")
print(result)