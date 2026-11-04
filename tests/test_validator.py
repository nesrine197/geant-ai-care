
from app.services.information_validator import validate_information


# Test 1: Complete information
complete_data = {
    "customer_intent": "troubleshooting",
    "product_type": "TV",
    "product_model": "GTV-43",
    "symptoms": [
        "black screen",
        "power light is on"
    ],
    "error_code": None,
    "conflicts": []
}


# Test 2: Missing model
incomplete_data = {
    "customer_intent": "troubleshooting",
    "product_type": "TV",
    "product_model": None,
    "symptoms": ["black screen"],
    "error_code": None,
    "conflicts": []
}


# Test 3: Vague symptoms
vague_data = {
    "customer_intent": "troubleshooting",
    "product_type": "TV",
    "product_model": "GTV-43",
    "symptoms": ["not working"],
    "error_code": None,
    "conflicts": []
}


for number, data in enumerate(
    [complete_data, incomplete_data, vague_data],
    start=1
):
    result = validate_information(data)

    print(f"\n===== TEST {number} =====")

    for key, value in result.items():
        print(f"{key}: {value}")
