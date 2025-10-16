// Server-related functions, all relatively similar to each other
async function listModels() {
    try {
        // Getting models
        const response = await fetch("/modelWork/list-models");
        // If it doesn't work, send error
        if (!response.ok) throw new Error("Server returned an error");
        // If it does work, then it continues
        // For later usage. Works compared to what was being used earlier.
        
        // Putting the data in a useable format.
        const dict = {};
        const values = response.json();
        const select = document.getElementById("modelSelect");
        values.then(resolved => {
            const models = resolved.models;
            Object.keys(models).forEach(name => {
                //console.log(`Added option: ${name}`); // Logs for when needed; not needed now.
                select.appendChild(new Option(name, name));
            });
        });
    }
    catch (err) {
        // Error handling
        console.error("Error listing models:", err);
        alert("Failed to fetch models.");
    };
};
async function sendPrompt() {
    try {
        const modelSelect = document.getElementById("modelSelect");
        const promptInput = document.getElementById("promptInput");
        const chat = document.getElementById("chat");

        chatBubble(promptInput.value, "user")
        const response = await fetch("/modelWork/send-prompt", { 
            method: "POST", 
            body: JSON.stringify({
                "chat":chat.value,
                "model":modelSelect.value,
                "prompt":promptInput.value
            }) 
        });
        const data = await response.json();
        chatBubble(data.response, "assistant")
    } catch (err) {
    console.error("Error sending prompt:", err);
    alert("Failed to send prompt. See console for details.");
    };
};
async function createModel(name, parent, sysMsg) {
    try {
        const response = await fetch("/modelWork/send-prompt", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                "name": name, 
                "parent": parent, 
                "sysMsg": sysMsg
            })
        });
    if (!response.ok) throw new Error("Server returned an error");
    const data = await response.json();
    const select = document.getElementById("modelSelect")
        for (let i = 0; i < data.models.length; i++) {
            select.appendChild(new Option(data.models[i], data.models[i]));
        }
        //console.log(data.models)
    } catch (err) { // Makes me want to create a separate area for reporting the errors for easier issue creation later.
        console.error("Error creating model:", err);
        alert("Failed to create model.");
    }
    // Pulling models so the user can use the new model
    listModels()
};

async function getHistory(chat = 0) {
    
    try {
        const response = await fetch("/modelWork/get-history", { 
            method: "POST", 
            body: JSON.stringify({
                "chat":chat
            }) 
        });
        const data = await response.json();
        return data["history"]
    } catch (err) {
    console.error("Error sending prompt:", err);
    alert("Failed to send prompt. See console for details.");
    };
}
window.addEventListener("DOMContentLoaded", async function() {
    listModels();

    chatDiv();
    // Chat setup; history gathering; temporary
    const chatData = await getHistory();
    for (let i = 0; i < chatData.length; i++) {
        let item = chatData[i];

        chatBubble(item[0]["content"],item[0]["role"]);
        chatBubble(item[1]["content"],item[1]["role"]);
    };
});

// Function for creating the message bubbles
function chatBubble(content, role) {
    if (typeof content !== "string" || typeof role !== "string") return false;

    const chatMessages = document.getElementById("chatMessages");
    if (!chatMessages) return false;

    const wrapper = document.createElement("div");
    const bubble = document.createElement("div");
    bubble.className = role === "user" ? "userMessage" : // If user, made to be user message
                       role === "assistant" ? "assistantMessage" : ""; // If assistant, made to be assistant message
    bubble.innerText = content;
    wrapper.appendChild(bubble);
    wrapper.className = "messageWrapper";
    chatMessages.appendChild(wrapper);
    return wrapper; // Returns the wrapper if needed in the future
};

// Function for creating the different chat divs
async function chatDiv() {
    let response = new Array();
    const chatList = document.getElementById("chatList");
    if (!chatList) {
        return // Can't be too careful, I guess.
    };

    for (let i = 0; i < 100; i++) {
        response = await getHistory(i);
        if (response.length > 0) {
            let chatItem = document.createElement("div");
            let butt = document.createElement("button");
            
            chatItem.classList.add("chatWrapper");
            butt.value = i;
            butt.innerText = "Chat "+(i+1);
            chatItem.appendChild(butt);
            chatList.appendChild(chatItem);
            butt.addEventListener("click", async function () {
                console.log("Button clicked");
                await selectChat(butt);
            });
        } else {
            break;
        }
    };
};

async function selectChat(elm) {
    document.getElementById("chatMessages").innerHTML = "";
    document.getElementById("chat").value = elm.value

    const hist = await getHistory(elm.value);

    for (let i = 0; i < hist.length; i++) {
        let item = hist[i];
        chatBubble(item[0]["content"],item[0]["role"]);
        chatBubble(item[1]["content"],item[1]["role"]);
    };
    return true
};

function createChat() {
    const chatList = document.getElementById("chatList");

    let newChatNum = chatList.children.length;

    let chatItem = document.createElement("div");
    let butt = document.createElement("button");

    butt.value = newChatNum;
    butt.innerText = "Chat "+(newChatNum+1);
    butt.addEventListener("click", async function () {
        console.log("Button clicked");
        await selectChat(butt);
    });
    chatItem.appendChild(butt);
    chatList.appendChild(chatItem);
};