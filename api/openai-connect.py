from openai import OpenAI
import json

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You analyze the responses to cold emails, discern if it is positive or negative response and whether the person is willing to continue the conversation, and make it into a boolean-wrapped json."},
    {"role": "user", "content": "Please analyze the text: Thank you for reaching out! I'm intrigued by your proposal and would love to learn more."},
    {"role": "user", "content": "Please analyze the text: While our current needs may not align with your offering, I have a colleague who might find it beneficial. Would you mind if I share your contact information with them?"},
  ]
)

completion2 = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "Given a response to a cold email, analyze it to determine if it is positive or negative response. Additionally, identify if the person expresses willingness to continue the conversation. Please format the results into a boolean-wrapped JSON."},
    {"role": "user", "content": "Please analyze the text: Thank you for your email. We currently have other priorities and are not looking to explore new solutions at this time."},
  ]
)

print(completion.choices[0].message)
print(completion2.choices[0].message)





