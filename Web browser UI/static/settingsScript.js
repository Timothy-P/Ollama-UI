async function settingRequest(elm = "", setting = "") {
    try {

        const response = await fetch("/settings/get-setting", { 
            method: "POST", 
            body: JSON.stringify({
                "elm":elm,
                "setting":setting
            }) 
        });
        const data = await response.json();
        //console.log(data["value"])
        //return JSON.stringify(data["value"]).replace("{", "{ ").replaceAll(":", " : ").replaceAll(","," , ").replace("}"," }");
        return data["value"]
    } catch (err) {
    console.error("Error getting setting:", err);
    alert("Failed to get setting. See console for details.");
    };
};

/*window.addEventListener("DOMContentLoaded", function() {
    this.document.getElementById("output").innerText = "&#8201;"
})*/

// Experimental, no idea if it'll work.
async function settingPresent() {
    // Gathering info
    elmVal = document.getElementById("elm").value;
    settingVal = document.getElementById("setting").value;

    // Getting the requested setting
    requestedSetting = await settingRequest(elmVal, settingVal);
    output = document.getElementById("settingsBox");

    // Clearing the box
    output.innerHTML = ""

    if (typeof requestedSetting == "string") { // If it's a string, just present it, though it'll have to be changed for what's coming next
        //output.innerText = `${elmVal} "${settingVal}"  = ${requestedSetting}`;
        alert("Setting is a string.\nThe setting:"+requestedSetting)
    }
    else if (typeof requestedSetting == "object") {
        //output.innerText = elmVal+":";
        for (let i = 0; Object.keys(requestedSetting).length > i; i++) { // Going though the different settings given from the server
            let currentKey = Object.keys(requestedSetting)[i];

            const p = document.createElement("p");
            p.style.gridColumn = "1";
            p.style.gridRow = parseInt(i+1);
            p.classList.add("settingsBoxP");
            p.innerText = currentKey

            const input = document.createElement("input");
            input.style.gridColumn = "2";
            input.style.gridRow = parseInt(i+1);
            input.setAttribute("parent", currentKey);
            input.value = requestedSetting[currentKey];
            // The functionality of it
            input.addEventListener("focusout", function () {
                settingModify(elmVal,currentKey,input.value);
            });

            output.appendChild(p);
            output.appendChild(input);

            // Currently reworking so it's not so messy/ugly
            //output.innerHTML += `<p style="grid-column:1;grid-row:${i+1};" class="settingsBoxP">${currentKey}</p>`
            //output.innerHTML += `<input style="grid-column:2;grid-row:${i+1};" value='`+requestedSetting[currentKey]+`'>` // Will give some sort of functionality as to how to send value later

            
            //output.innerHTML += "<br>    "+currentKey+": "+requestedSetting[currentKey];
        };
        
    }
    else {
        console.error("Error: 'requestedSetting' is not a valid data type ("+typeof requestedSetting+")");
        alert("Error occured. Check console for details.")
    };
}

async function settingModify(object,setting,newValue) {
    try {

        const response = await fetch("/settings/edit-settings", { 
            method: "POST", 
            body: JSON.stringify({
                "elm":object,
                "setting":setting,
                "newVal":newValue
            })
        });
        const data = await response.json();

        // Updates CSS
        const link = document.getElementById("CSS");
        const url = new URL(link.href);
        url.searchParams.set("v", Date.now()); // unique each time
        link.href = url.toString();

        return data["value"];
    } catch (err) {
        console.error("Error getting setting:", err);
        alert("Failed to get setting. See console for details.");
    };
}


function enterPressed(event) {
    // Literally it. Just submitting if enter is pressed.
    if (event["key"] === "Enter") settingPresent()
}