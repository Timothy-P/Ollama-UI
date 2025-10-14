async function settingRequest() {
    try {
        const elm = document.getElementById("elm");
        const setting = document.getElementById("setting");
        const output = document.getElementById("output");

        const response = await fetch("/settings/get-setting", { 
            method: "POST", 
            body: JSON.stringify({
                "elm":elm.value,
                "setting":setting.value
            }) 
        });
        const data = await response.json();

        output.innerText = JSON.stringify(data["value"]).replace("{", "{ ").replaceAll(":", " : ").replaceAll(","," , ").replace("}"," }");
    } catch (err) {
    console.error("Error getting setting:", err);
    alert("Failed to get setting. See console for details.");
    };
};

window.addEventListener("DOMContentLoaded", function() {
    settingRequest();
})