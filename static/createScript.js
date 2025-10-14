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
async function createModel() {
    const sysMsg = document.getElementById("sysPrompt").value
    const name = document.getElementById("modelName").value
    const parent = document.getElementById("modelSelect").value
    
    try {
        const response = await fetch("/modelWork/create-model", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                "name": name, 
                "parent": parent, 
                "sysMsg": sysMsg
            })
        });
    if (!response.ok) throw new Error("Server returned an error");

    } catch (err) { // Makes me want to create a separate area for reporting the errors for easier issue creation later.
        //console.error("Error creating model:", err);
        //alert("Failed to create model.");
        try {
            await fetch("/sys/logs", {
                method: "POST",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify({
                    "Error":err
                })
            });
        } catch(error) {
            console.log("Could not post for system log:"+error);

        }
    };

    // Pulling models so the user can use the new model
    listModels();
};
window.addEventListener("DOMContentLoaded", function() {
    listModels();
});