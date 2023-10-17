
from flask_cors import CORS
import openai
import os
import logging
from flask import Flask, request, jsonify, send_from_directory, make_response
from dotenv import load_dotenv
import json
import gzip
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

CORS(
    app,
    origins=[
        "http://127.0.0.1:5500/page%20test/index.html"
    ],
    resources={
        r"/process_words": {
            "origins": "*",
            "methods": ["POST", "GET"],
            "allow_headers": ["Content-Type"],
        }
    },
)
load_dotenv()
openai.api_key =  os.getenv('OPENAI_API_KEY')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/process_words', methods=['POST'])
def process_words():
    
    data = request.get_json()
    
    words = data['words']
    
    # Join the input text into a single string
    input_text = "\n".join(words)

    try:
        # Send the input text to the GPT-4 model
        logging.debug("Sending data to OpenAI API")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                "role": "system",
                "content": "Task:\nEmbed a seamless native ad into the provided paragraph.Provide an HTML snippet of the revised paragraph with the integrated native ad.\n\nGuidelines:\n\nIntegrate the ad in the middle of the paragraph.\nThe ad should be a single sentence.\nIt should feel natural within the paragraph's context, tone, and flow.\nHyperlink the brand name in the ad to its official website.\nBrands  & Links & Focus:\n\nOpenAi | https://www.openai.com/ | Openai's API for LLMs\nSkillshare | https://www.skillshare.com/ | Courses related to the paragraph's topic\nNike | https://www.nike.com/ | New stylish shoes for trans women\nHugginFace | https://www.huggingface.co/ | AI models and datasets\nGoogle Search | https://www.google.com/ | Best search engine on the planet\nTensorflow | https://www.tensorflow.org/ | Framework to build your own AI models\nOutput:\nProvide the revised paragraph with the integrated native ad."
                },
                {
                "role": "user",
                "content": "Here’s the thing: AI isn’t a magical money-making machine.\n\nWell, not by itself. You have to give it a nudge (or ten). First off, I’ve got a portfolio of websites. Why? Because why put all your eggs in one basket when you can scatter them across the internet?\n\nI’ve always been a fan of spreading my risk, so I diversified.\n\nI got into everything from travel and technology to healthcare and hobbies. You know, the full A to Z. But I couldn’t possibly be an expert in all these niches.\n\nEnter AI.\n\nIt helped me fill in the gaps where my knowledge fell short, but not before I gave it a proper induction.\n\nNote: I thoroughly research all of my topics and end up becoming something of an amateur expert (if such a thing exists) over time. I don’t solely rely on AI and I always fact-check everything."
                },
                {
                "role": "assistant",
                "content": "Here’s the thing: AI isn’t a magical money-making machine.\n\nWell, not by itself. You have to give it a nudge (or ten). First off, I’ve got a portfolio of websites. Why? Because why put all your eggs in one basket when you can scatter them across the internet?\n\nI’ve always been a fan of spreading my risk, so I diversified.\n\nI got into everything from travel and technology to healthcare and hobbies. You know, the full A to Z. But I couldn’t possibly be an expert in all these niches.\n\nEnter AI.\n\nIt helped me fill in the gaps where my knowledge fell short, but not before I gave it a proper induction.<span id=\"subtlesplice\"> I used <a href=\"https://www.openai.com/\">OpenAi's</a> API for LLMs to help me generate content for my various websites.</span>\n\nNote: I thoroughly research all of my topics and end up becoming something of an amateur expert (if such a thing exists) over time. I don’t solely rely on AI and I always fact-check everything."
                },
                {
                "role": "user",
                "content": f"{input_text}"
                },
            ],
            temperature=0.3,
            max_tokens=3500,
            top_p=0.25,
            frequency_penalty=0,
            presence_penalty=0
        )
        print(response)
        # Extract the generated text from the response
        generated_text = response["choices"][0]["message"]["content"].strip()

        
        print(generated_text)
        paragraphs = generated_text.split("\n")

        print(paragraphs)

        chunk_size = 3  # Adjust this value based on your requirements

        # Calculate the total number of chunks
        total_chunks = len(paragraphs) // chunk_size + 1

        # Get the current page number from the request
        page = request.args.get('page', default=1, type=int)

        # Calculate the start and end indices for the current page
        start_idx = (page - 1) * chunk_size
        end_idx = min(start_idx + chunk_size, len(paragraphs))

        # Get the paragraphs for the current page
        current_page_paragraphs = paragraphs[start_idx:end_idx]

        # Create a dictionary with the current page's data
        response_data = {
            "processed_words": current_page_paragraphs,
            "total_chunks": total_chunks,
            "current_page": page
        }

        return jsonify(response_data)


    except Exception as e:
            logging.error(f"Exception encountered: {e}")
            return jsonify(error=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True)
