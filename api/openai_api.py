from openai import OpenAI
import json

def get_openai_client():
  return OpenAI(
    api_key="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"
  )

def get_feedback(client, text):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You analyze responses to cold emails sent for job offers, discern if it is positive or negative response and whether the person is willing to continue the conversation, and make it into a JSON-wrapped boolean. Here is how your JSON answer should look like: ```{positive: true}```\nor ```{positive: false}```"},
      {"role": "user", "content": f"Please analyze the text: {text}"},
    ]
  )
  reply = completion.choices[0].message
  # TODO check for mistakes in the reply
  return json.loads(reply)