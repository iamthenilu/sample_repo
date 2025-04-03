from flask import Flask, request, jsonify, render_template
# from langchain.chat_models import ChatVertexAI
# from langchain.schema import HumanMessage

app = Flask(__name__)

# Initialize LLM
# chat_model = ChatVertexAI()

@app.route('/')
def home():
    return render_template(r'chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Get response from VertexAI
    # response = chat_model([HumanMessage(content=user_message)])
    # reply = response.content if response else "Sorry, I didn't understand that."
    reply = "this is a reply"
    return jsonify({"response": reply})

if __name__ == '__main__':
    app.run(debug=True)
