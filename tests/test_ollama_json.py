from app.services.ollama import generate_structured_response

prompt = """
Extract the product type and model from the customer message.

Return JSON with exactly these fields:
{
    "product_type": "string or null",
    "product_model": "string or null"
}
"""

conversation = [
    {
        "role": "user",
        "content": "My refrigerator smells like something is burning. Its model is GTV-450."
    }
]

result = generate_structured_response(
    conversation,
    prompt
)

print("\nMINIMAL JSON TEST:")
print(result)