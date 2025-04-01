import base64
import requests
import os
from mistralai import Mistral

def encode_image(image_path):
	"""Encode the image to base64."""
	try:
		with open(image_path, "rb") as image_file:
			return base64.b64encode(image_file.read()).decode('utf-8')
	except FileNotFoundError:
		print(f"Error: The file {image_path} was not found.")
		return None
	except Exception as e:  # Added general exception handling
		print(f"Error: {e}")
		return None

# Specify model
model = "pixtral-12b-2409"
# Initialize the Mistral client
client = Mistral(api_key=api_key)


def extract_receipt_data(image_path):

  # Getting the base64 string
  base64_image = encode_image(image_path)

  # Define the messages for the chat
  messages = [
	  {
		  "role": "user",
		  "content": [
			  {
				  "type": "text",
				  "text": """You are a financial expert assistant. Analyze this bank receipt (image) and extract only the following information in JSON format:
						- The **date** of the transaction (in the format DD/MM/YYYY).
						- The **total amount** of the receipt (in the exact amount, using a period as the decimal separator).
      						-  The **currency** of the total amount.
						- The **vendor's address** presented in a complete sentence.
					If any of the information cannot be found, return `null` for that field."""
			  },
			  {
				  "type": "image_url",
				  "image_url": f"data:image/jpeg;base64,{base64_image}"
			  }
		  ]
	  }
  ]

  # Get the chat response
  chat_response = client.chat.complete(
	  model=model,
	  messages=messages
  )
  return chat_response.choices[0].message.content
  
  
  
 print(extract_receipt_data(rcp1))
