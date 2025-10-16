if __name__ != "__main__":
    print("This is not supposed to be run as a module.\nTry again by running `python3 app.py` or `python app.py`, depending on your version of Python.")
from flask import Flask, render_template, jsonify, request
import webbrowser
from interact import *
from settings import Settings
import json
app = Flask(__name__)

# The pages
@app.route("/")
def index():
    return render_template("index.html")

# Sub pages
@app.route("/settings")
def settings():
    return render_template("settings.html")
@app.route("/interact")
def interact():
    return render_template("interact.html")
@app.route("/create")
def create():
    return render_template("create.html")

# The functions

# System function
@app.route("/sys/end-session")
def end_session():
    setts.saveSettings("saveTest.txt")
    exit()

# Model interaction functions
hist = History("chat.txt")
@app.route("/modelWork/list-models") # Done
async def list_models_route():
    models = await listModels()
    return jsonify({"models": models})

@app.route("/modelWork/send-prompt", methods=["POST"]) # Done
async def send_prompt_route():
    data = json.loads(request.data)
    print(data)
    model = data["model"]
    prompt = data["prompt"]
    chat = data["chat"]
    if type(model) == str and type(prompt) == str and type(chat) == str:
        response = await sendPrompt(model, prompt, int(chat))
        #add([{"role":"user","content":prompt},{"role":"assistant","content":"response"}], int(chat)) # Works

        saveHistory("chat.txt") # Works

        return jsonify({"status":"success","response": response})
    
    saveHistory("chat.txt")

    return jsonify({"status":"failure"})

@app.route("/modelWork/create-model", methods=["POST"]) # Done
async def create_model_route():
    data = json.loads(request.data)
    name = data["name"]
    parent = data["parent"]
    sysMsg = data["sysMsg"]

    if await createModel(name,parent,sysMsg):
        return jsonify({"status": "success"})
    else:
        return jsonify({"status":"failure"})

@app.route("/modelWork/running", methods=["POST"]) # Done
def running_route():
    return jsonify(running())

# History-related
@app.route("/modelWork/get-history", methods=["POST"])
def get_history_route():
    data = json.loads(request.get_data())
    chat = data["chat"]
    getHistory(chat)
    return jsonify({"status":"success", "history":getHistory(chat)})
@app.route("/modelWork/remove-history", methods=["POST"]) # Done
def remove_history_route():
    item = request.form.get("item")
    chat = request.form.get("chat")
    if type(item) == str and type(chat) == str:
        if removeHistory(int(item), int(chat)):
            return jsonify({"status":"success"})
        else:
            return jsonify({"status":"failure"})
    return jsonify({"status":"failure"})
    
@app.route("/modelWork/edit-history", methods=["POST"]) # Done
def edit_history_route():
    chat = request.form.get("chat")
    role = request.form.get("role")
    item = request.form.get("item")
    newVal = request.form.get("newVal")
    if type(chat) == str and type(role) == str and type(item) == str and type(newVal) == str:
        if editHistory(int(item), newVal, int(chat), role):
            return jsonify({"status":"success"})
        else:
            return jsonify({"status":"failure"})
    return jsonify({"status":"failure"})
    
@app.route("/modelWork/remove-model", methods=["POST"]) # Done
def remove_model_route(model:str):
    if rmModel(model):
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"failure"})

# Setting functions
setts = Settings()
@app.route("/settings/load-settings", methods=["POST"]) # Done
def load_settings_route():
    file = request.form.get("file")
    if type(file) == str:
        if setts.loadSettings(file):
            return jsonify({"status":"success","settings":setts.showSetting()})
    return jsonify({"status":"failure"})

@app.route("/settings/edit-settings", methods=["POST"]) # Done
def edit_settings_route():
    setting = request.form.get("setting")
    newVal = request.form.get("newVal")
    elm = request.form.get("elm")
    if type(setting) == str and type(newVal) == str and type(elm) == str:
        if setts.editSetting(elm, setting,newVal):
            return jsonify({"status":"success"})
    return jsonify({"status":"failure"})
    
@app.route("/settings/delete-setting", methods=["POST"]) # Done
def delete_setting_route():
    setting = request.form.get("setting")
    if type(setting) == str:
        if setts.rmSetting(setting):
            return jsonify({"status":"success"})
    return jsonify({"status":"failure"})

@app.route("/settings/get-setting", methods=["POST"])
def get_setting_route():
    data = json.loads(request.data)
    elm = data["elm"]
    setting = data["setting"]
    if type(elm) == str and type(setting) == str:
        value = setts.showSetting(elm, setting)
        return jsonify({"status": "success", "value": value})
    return jsonify({"status": "failure"})


# Logs because it's being ridiculous. >:(
@app.route("/sys/logs", methods=["POST"])
def logs_route():
    print("System logs:")
    print(f"    Logs received: {request.get_data()}")
    with open("ollamaMenu.logs", "a") as file:
        if file.writable:
            file.write(str(json.loads(request.get_data()))+"\n")
        else:
            print("    Log file not writeable.")
        file.close()

    return jsonify({"status":"success"})

webbrowser.open("http://127.0.0.1:5000/")

app.run(debug=False)