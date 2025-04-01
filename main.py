import base64
import requests
import os
import csv
import json 
import re
from mistralai import Mistral


api_key = os.getenv("API_KEY")


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
						- The **date** of the transaction (in the format YYYY-MM-DD).
						- The **total amount** of the receipt (in the exact amount, using a period as the decimal separator).
      					-  The **currency** of the total amount.
						- The **vendor's address** presented directly as a complete sentence, with no additional text like 'the vendor address is.'
					If any of the information cannot be found, return `null` for that field. """
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


rcp = "receipts/1000-receipt.jpg"
#extracted_data = extract_receipt_data(rcp)
#print("extracted_data is : ",extracted_data.strip())


def process_images_in_directory(directory_path, output_csv_path,limit_files):
	"""Process all images in the given directory and save the results in a CSV."""
	# Prepare to write to CSV
	fieldnames = ["filename", "date", "amount", "currency", "vendor_address"]
	
	with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writeheader()

		# Loop through all files in the directory
		for filename in os.listdir(directory_path)[:limit_files]:
			if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Only process image files
				image_path = os.path.join(directory_path, filename)
				print(f"Processing {filename}...")

				# Extract data from the image
				extracted_data = extract_receipt_data(image_path)

				if extracted_data:
					match = re.search(r"\{.*\}",extracted_data, re.DOTALL)
					try:
						if match : 
							json_text = match.group(0)
							data = json.loads(json_text)
	
							# Prepare row for CSV
							row = {
								"filename": filename,
								"date": data.get("date", None),
								"amount": data.get("amount", None),
								"currency": data.get("currency", None),
								"vendor_address": data.get("vendor_address", None)
							}
	
							# Write row to CSV
							writer.writerow(row)
					except json.JSONDecodeError:
						print(f"Error decoding JSON for {filename}. Skipping this file.")
				else:
					print(f"No data extracted for {filename}.")

# Specify the directory containing the receipts
directory_path = 'receipts'  # Replace with your actual directory path
output_csv_path = 'extracted_receipts_data.csv'

# Process the images and save the results in a CSV
process_images_in_directory(directory_path, output_csv_path,3)
print("Processing complete! Data has been saved to the CSV file.")
