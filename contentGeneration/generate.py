import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
from flask import url_for

load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_instagram_post(form_data, files, app):
    caption = form_data.get('caption', '')
    hashtags = form_data.get('hashtags', '').split(',')
    schedule = form_data.get('schedule', '')

    # Handle file uploads
    uploaded_files = files.getlist('media')
    filenames = []
    image_urls = []

    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            filenames.append(filename)

            # Generate the correct URL for the uploaded file
            with app.app_context():
                image_url = url_for('uploaded_file', filename=filename, _external=True)
                image_urls.append(image_url)

    # Prepare the messages for OpenAI API
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that generates engaging Instagram captions with appropriate format and optimizes hashtags."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Generate an engaging Instagram caption based on the following input: {caption}\n\nCurrent hashtags: {', '.join(hashtags)}\n\nPlease optimize the caption, add more relevant hashtags if needed, and ensure the total number of hashtags is between 5 and 30. Format the response as: CAPTION: [generated caption] HASHTAGS: [list of hashtags]"
                }
            ]
        }
    ]

    # Add image URLs to the message
    for url in image_urls:
        messages[1]["content"].append({
            "type": "image_url",
            "image_url": {"url": url}
        })

    # Make a single API call to OpenAI
    completion = client.chat.completions.create(
        model="gpt-4o",  
        messages=messages,
        max_tokens=300,
    )

    response_content = completion.choices[0].message.content.strip()
    
    # Split the response into caption and hashtags
    caption_part, hashtags_part = response_content.split("HASHTAGS:")
    generated_caption = caption_part.replace("CAPTION:", "").strip()
    optimized_hashtags = [tag.strip() for tag in hashtags_part.split() if tag.strip()]

    # Combine generated caption with hashtags
    final_caption = f"{generated_caption}\n\n{' '.join(optimized_hashtags)}"

    # Schedule the post (you'll need to implement this part based on your needs)
    scheduled_time = datetime.strptime(schedule, '%Y-%m-%d %H:%M')

    # Here you would typically save the post details to a database
    # and set up a task to publish it at the scheduled time

    return {
        'status': 'success',
        'message': 'Post generated successfully',
        'caption': final_caption,
        'media': filenames,
        'scheduled_time': scheduled_time.isoformat()
    }

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}