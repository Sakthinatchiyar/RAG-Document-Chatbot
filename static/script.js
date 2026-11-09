
async function sendMessage() {

    const input = document.getElementById("question");
    const chatBox = document.getElementById("chatBox");
    const mode = document.getElementById("mode").value;

    const question = input.value.trim();

    if (!question) {
        alert("Please enter a question.");
        return;
    }

    addMessage(question, "user");
    input.value = "";

    const loading = addMessage("Thinking...", "bot");

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question,
                mode: mode
            })

        });

        const data = await response.json();

        loading.remove();

        if (!response.ok) {
            throw new Error(data.answer || "Request failed.");
        }

        const answer = addMessage(data.answer, "bot");

        if (data.sources && data.sources.length > 0) {

            const sourceText = document.createElement("div");

            sourceText.className = "sources";

            const uniqueSources = [
                ...new Map(
                    data.sources.map(item => [
                        `${item.source}-${item.page}`,
                        item
                    ])
                ).values()
            ];

            sourceText.textContent = "Sources: " +
                uniqueSources.map(
                    item => `${item.source}, page ${item.page}`
                ).join(" | ");

            answer.appendChild(sourceText);
        }

    } catch (error) {

        loading.remove();
        addMessage("Error: " + error.message, "bot");

    }

    chatBox.scrollTop = chatBox.scrollHeight;
}


function addMessage(text, type) {

    const chatBox = document.getElementById("chatBox");

    const message = document.createElement("div");

    message.className = "message " + type;
    message.textContent = text;

    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;

    return message;
}


// Send question when Enter is pressed
document.getElementById("question").addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {
            sendMessage();
        }

    }
);
