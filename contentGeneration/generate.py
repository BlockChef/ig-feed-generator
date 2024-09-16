import os
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI
from werkzeug.utils import secure_filename

load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_instagram_post(form_data, files, app):
    caption = form_data.get("caption", "")
    hashtags = form_data.get("hashtags", "").split(",")
    schedule = form_data.get("schedule", "")

    # Handle file uploads
    uploaded_files = files.getlist("media")
    filenames = []

    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            filenames.append(filename)

    # Prepare the messages for OpenAI API
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that generates engaging Instagram captions with appropriate format and optimizes hashtags.",
        },
        {
            "role": "user",
            "content": f"Generate an engaging Instagram caption based on the following input: {caption}\n\nCurrent hashtags: {', '.join(hashtags)}\n\nPlease optimize the caption, add more relevant hashtags if needed, and ensure the total number of hashtags is between 5 and 30. Format the response as: CAPTION: [generated caption] HASHTAGS: [list of hashtags]",
        },
    ]

    try:
        # Make a single API call to OpenAI
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=300,
        )

        response_content = completion.choices[0].message.content.strip()

        # Split the response into caption and hashtags
        caption_part, hashtags_part = response_content.split("HASHTAGS:")
        generated_caption = caption_part.replace("CAPTION:", "").strip()
        optimized_hashtags = [
            tag.strip() for tag in hashtags_part.split() if tag.strip()
        ]

        # Combine generated caption with hashtags
        final_caption = f"{generated_caption}\n\n{' '.join(optimized_hashtags)}"

        # Schedule the post (you'll need to implement this part based on your needs)
        scheduled_time = (
            datetime.strptime(schedule, "%Y-%m-%d %H:%M") if schedule else None
        )

        return {
            "status": "success",
            "message": "Post generated successfully",
            "caption": final_caption,
            "media": filenames,
            "scheduled_time": scheduled_time.isoformat() if scheduled_time else None,
        }
    except Exception as e:
        print(f"Error in API call: {str(e)}")
        raise Exception(f"Error in generating post: {str(e)}")


def revise_instagram_post(post_data, suggestion, app):
    # Prepare the messages for OpenAI API
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that revises Instagram captions based on user suggestions.",
        },
        {
            "role": "user",
            "content": f"Revise the following Instagram caption based on this suggestion: {suggestion}\n\nCurrent caption: {post_data['caption']}\n\nPlease provide the revised caption and hashtags. Format the response as: CAPTION: [revised caption] HASHTAGS: [list of hashtags]",
        },
    ]

    try:
        # Make a single API call to OpenAI
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=300,
        )

        response_content = completion.choices[0].message.content.strip()

        # Split the response into caption and hashtags
        caption_part, hashtags_part = response_content.split("HASHTAGS:")
        revised_caption = caption_part.replace("CAPTION:", "").strip()
        revised_hashtags = [tag.strip() for tag in hashtags_part.split() if tag.strip()]

        # Combine revised caption with hashtags
        final_caption = f"{revised_caption}\n\n{' '.join(revised_hashtags)}"

        # Update the post_data with the revised caption
        post_data["caption"] = final_caption

        return post_data
    except Exception as e:
        print(f"Error in API call: {str(e)}")
        raise Exception(f"Error in revising post: {str(e)}")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "png",
        "jpg",
        "jpeg",
        "gif",
        "mp4",
        "mov",
    }
