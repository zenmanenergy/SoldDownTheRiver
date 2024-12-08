

# Set your OpenAI API key
import openai
import json

# Set your OpenAI API key
openai.api_key = ''

# Define the prompt (input text)
prompt = (
    "Convert the following text into a JSON object:\n"
    "Text: 'Boudar put one of Pascal's slaves up for sale at the New Exchange Coffee House, "
    "on the corner of St. Lewis and Charles Street. Lockett was the highest bidder at $725 "
    "for a negro girl named Clarissa aged about 11. Clarissa was originally brought from Norfolk, Virginia by Pascal.'\n"
    "Please extract and format the data as JSON with the following keys: seller, buyer, price, currency, location (venue, address), individual (name, age, status, origin (city, state)), previous_owner."
)

# Function to generate text from OpenAI using the new API format
def generate_text_with_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the appropriate model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

# Generate the text using OpenAI's API
generated_text = generate_text_with_openai(prompt)

# Print the generated text (for debugging)
print("Generated Text:", generated_text)

# # Parse the generated text into a JSON object
# try:
#     data = json.loads(generated_text)
#     # Print the resulting JSON
#     print(json.dumps(data, indent=2))
# except json.JSONDecodeError as e:
#     print("Failed to decode JSON:", e)
