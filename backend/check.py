import os
import openai
import tiktoken

# Set the base URL and api_key for the RDSec One AI Endpoint API (Production)
# Use the python-dotenv to load variables from env 
openai.base_url = "https://api.rdsec.trendmicro.com/prod/aiendpoint/v1/"
openai.api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiQUktMTczNDUzODcyODAyMiIsInJvbGVzIjpbIjM1Il0sInVzZXJfaWQiOjE0ODMsInVzZXJuYW1lIjoibWVldHMiLCJyb2xlX25hbWVzIjpbIlJPUC1haWVuZHBvaW50LVVzZXIiXSwidG9rZW5fdHlwZSI6ImFjY2VzcyIsImV4cCI6MTc0MjMxNDcyOCwianRpIjoiYzMwZDQzMGEtYmQ1Yi0xMWVmLWIxYTYtYjY3YjcyNDViYjEwIiwidmVyc2lvbiI6IjIwMjQtMTEtMDEifQ.sDHxLKk9_3AUHCYQGP63a1GMfOeGucObc4O99AgyDNE"
openai.api_type = "openai"
model = "gpt-4o"

# Define the prompt to be sent to the OpenAI API
prompt = "What is the capital of France?"

# Send a chat completion request to the OpenAI API
# The model used is "gpt-4o"
# The message sent is the defined prompt
response = openai.chat.completions.create(
    model=model,
    messages=[
        {"role": "user", "content": prompt},
    ],
)

# Get the encoding for the model and calculate the token usage
encoding = tiktoken.encoding_for_model(model)
input_tokens = encoding.encode(prompt)
output_tokens = encoding.encode(response.__str__())

# Extract the content of the first choice from the response
response_text = response.choices[0].message.content

# Print the prompt and the response from the OpenAI API
print(f"Your Prompt is : {prompt}")
print(f"Format AI Endpoint Response: {response_text}")
print(f"Token Usage: completion_tokens:{len(output_tokens)} | prompt_token:{len(input_tokens)} | total_tokens:{len(input_tokens) + len(output_tokens)}")