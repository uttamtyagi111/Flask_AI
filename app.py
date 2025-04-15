# kindly read these commands carefully before running the code.
# To run this app, save this code in a file named app.py and run it using the command:
# before running the command, make sure you are in virtual environment and have Flask installed.
# python app.py

#####Testing the API Endpoint#####
#We can use postman,RapidAPI, or any other API testing tool to test the endpoint.
# you can then send a POST request to the endpoint  http://127.0.0.1:5000/generate_explanation with a JSON body containing the 'grade' and 'concept' fields.
# Example request body:
# {
#     "grade": 8,
#     "concept": "newton's first law"
# }
# the server will respond with a JSON object containing the prompt, generated explanation, and word count.

from flask import Flask, request, jsonify

app = Flask(__name__)

def simulate_ai_response(prompt):
    responses = {
        "newton's first law": {
            8: "Newton's First Law states that an object at rest stays at rest, and an object in motion stays in motion with the same speed and direction, unless acted upon by an outside force. Think about riding a skateboard - you'll keep rolling until something stops you, like friction or a wall. Or when you're sitting on a chair, you stay put until you decide to get up and apply a force to move.",
            5: "Newton's First Law means things don't change how they're moving unless something pushes or pulls them. If your toy car is stopped, it stays stopped until you push it. If it's rolling, it keeps rolling until something stops it, like the carpet or your hand.",
            11: "Newton's First Law of Motion, also known as the Law of Inertia, states that an object will maintain its state of rest or uniform motion in a straight line unless acted upon by an external force. This fundamental principle explains why passengers in a vehicle lurch forward when the driver suddenly brakes, or why a book remains stationary on a desk until moved. The law quantifies our understanding of inertia - the resistance of any physical object to a change in its velocity."
        },
        "photosynthesis": {
            8: "Photosynthesis is how plants make their own food using sunlight. Plants take in carbon dioxide from the air and water from the soil. Then, with the help of sunlight and a green substance called chlorophyll, they convert these ingredients into glucose (sugar) and oxygen. The plant uses the glucose for energy to grow, and releases the oxygen into the air, which we breathe!",
            5: "Photosynthesis is like a plant's way of cooking its own food! Plants drink water from the ground and breathe in air. Then they use sunlight as energy to turn water and air into food. The plants eat this food to grow and give us oxygen that we need to breathe.",
            11: "Photosynthesis is the biochemical process by which plants, algae, and certain bacteria convert light energy, typically from the sun, into chemical energy in the form of glucose. This process occurs primarily in the chloroplasts, specifically in the thylakoid membranes, where chlorophyll molecules capture photons. The process can be summarized by the equation: 6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂, representing how carbon dioxide and water, in the presence of light, produce glucose and oxygen."
        }
    }
    
    words = prompt.lower().split()
    concept = ""
    grade = 8 
    
    for c in ["newton's first law", "photosynthesis"]:
        if c in prompt.lower():
            concept = c
    
    for i, word in enumerate(words):
        if word == "grade" and i+1 < len(words) and words[i+1].isdigit():
            grade = int(words[i+1])
    
    available_grades = list(responses.get(concept, {}).keys())
    if grade not in available_grades and available_grades:
        grade = min(available_grades, key=lambda x: abs(x - grade))
    
    return responses.get(concept, {}).get(grade, "I would explain this concept by breaking it down into simple terms the student can understand, using everyday examples they would be familiar with. I'd use clear language appropriate for their grade level, avoiding unnecessary technical terms.")

@app.route('/generate_explanation', methods=['POST'])
def generate_explanation():
    data = request.get_json()

    if not data or 'grade' not in data or 'concept' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        grade = int(data['grade'])
        concept = str(data['concept'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid data types'}), 400
    
    prompt = f"Explain {concept} in simple words for a {grade}th-grade student. Use relatable examples."
    explanation = simulate_ai_response(prompt)
    word_count = len(explanation.split())
    
    response = {
        "prompt": prompt,
        "generated_explanation": explanation,
        "word_count": word_count
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
    
    
