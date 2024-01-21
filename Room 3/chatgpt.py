import openai

# Set your OpenAI GPT-3 API key here
api_key = "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"

# Prompt for the GPT-3 model
prompt = "Pretend you are a resident annoyed at a Foodpanda delivery man. Give me a one sentence sentence of annoyance or mockery (max 10 words) to the delivery man."

# OpenAI API request
response = openai.Completion.create(
  engine="gpt-3.5-turbo",
  prompt=prompt,
  max_tokens=50,
  api_key=api_key
)

# Extract and print the generated praise
insult = response['choices'][0]['text'].strip()
print(insult)
