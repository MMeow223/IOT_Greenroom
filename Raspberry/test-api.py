import requests
import base64

# Set the path to your image file
image_path = "C:/Users/Asus/Documents/Arduino/greenroom_unit/Raspberry/WIN_20231018_16_21_30_Pro.jpg"


# Read the image file as bytes and encode it in base64
with open(image_path, "rb") as file:
    image_base64 = base64.b64encode(file.read()).decode("utf-8")
print(image_base64)

# Set the API key, project ID, and model version
api_key = "9TwZaDpIJ3gnWQ0inEaH"
project_id = "plant-size-zrqp4"
version_id = "2"

# Set the API endpoint URL
api_url = f"https://detect.roboflow.com/{project_id}/{version_id}"

# Set parameters for the request (API key)
params = {
    "api_key": api_key
}

# Set headers including the content type
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Set data as base64-encoded image
data = {
    "image": image_base64
}

# Make the API request
try:
    response = requests.post(api_url, params=params, headers=headers, data=data)
    response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e.response.status_code}, {e.response.text}")
    raise
except requests.exceptions.RequestException as e:
    print(f"Error making API request: {e}")
    raise

# Check the response
if response.status_code == 200:
    # Print the JSON response
    print(response.json())
else:
    print(f"Error: {response.status_code}, {response.text}")
