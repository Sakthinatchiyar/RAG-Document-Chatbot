
from flask import Flask, render_template, request, jsonify
from rag import generate_answer

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    question = data.get("question", "").strip()
    mode = data.get("mode", "with_rag")

    if not question:
        return jsonify({
            "answer": "Please enter a question.",
            "sources": []
        }), 400

    use_rag = mode == "with_rag"

    result = generate_answer(
        question,
        use_rag=use_rag
    )

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
