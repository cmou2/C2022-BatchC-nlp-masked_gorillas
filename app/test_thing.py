
import openai

openai.api_key = "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"

response = openai.Completion.create(
  model="ada:ft-personal-2022-07-31-18-04-47",
  prompt="I am feeling sad.",
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
print(response)