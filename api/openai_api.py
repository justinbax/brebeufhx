from openai import OpenAI
import os
import json

def get_openai_client():
  # TODO error handling
  return OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
  )

def get_feedback(client, text):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You analyze responses to cold emails sent for job offers, discern if it is positive or negative response and whether the person is willing to continue the conversation, and make it into a JSON-wrapped boolean. Here is how your JSON answer should look like: ```{\"positive\": true}```\nor ```{\"positive\": false}```"},
      {"role": "user", "content": f"Please analyze the text: {text}"},
    ]
  )
  reply = completion.choices[0].message.content
  # TODO check for mistakes in the reply
  print(reply)
  result = json.loads(reply)
  
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You analyze responses to cold emails sent for job offers, discern if it is positive or negative response and whether the person is willing to continue the conversation. You give a one-sentence summary of the email's emotion and of its message."},
      {"role": "user", "content": f"Please analyze the text: {text}"},
    ]
  )
  result["analysis"] = completion.choices[0].message.content

  return result