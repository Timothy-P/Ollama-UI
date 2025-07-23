# This is how I'll do the interactions between the user and model.
import requests, subprocess

ollamaURL = "http://localhost:11434/api/generate"

def sendPrompt(model: str, prompt: str):
    response = requests.post(ollamaURL, json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    if response.ok:
        return response.json()["response"]
    else:
        return f"Error: {response.text}"


def listModels():
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    if result.returncode == 0:
        #data = json.loads(result.stdout)
        #return [model["name"] for model in data["models"]]
        filtered = result.stdout.split("\n")
        filteredMore = []
        for i in range(1, len(filtered)-1):
            filteredMore.append(filtered[i].split(":")[0])
        return filteredMore
    else:
        print("Failed to list models.")
        print(result.stderr)
        return []

if __name__ == "__main__":
    print("Please run \"main.py\" as opposed to this file.")
    exit()