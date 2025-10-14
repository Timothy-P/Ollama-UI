"""
A simple way of interacting with Ollama.

The many functions are for a pre-made `History` variable, but you can also create your own.

Some other functions are for interacting with Ollama itself, like removing, listing, or creating models.
"""

import ollama, json

# Basic functions
async def listModels() -> dict[str, dict[str, str]]:
    """
    Returns a dictionary of the models.
    """
    modelData = ollama.list()
    returnData:dict[str, dict[str, str]] = {}
    for i in modelData['models']:
        # Only getting the important stuff. The rest doesn't matter to me.
        # However, if you do need this, for whatever reason, then good luck.
        # I don't regret making it as much as all the information being totally useless because I don't ever need it.
        returnData[i['model'].split(":")[0]] = {"parent":i['details']['family'], "parameter-size":i['details']['parameter_size'], "quantization":i['details']['quantization_level'], "format":i['details']['format']}
    return returnData

async def createModel(model:str, parent:str, sysMsg:str) -> bool:
    """
    Creates a model, returning a bool depending on the status.
    """
    # Ensuring the parent is a valid model
    if parent in await listModels():
        ollama.create(model=model, from_=parent, system=sysMsg)
        return True
    return False
    
async def rmModel(model:str) -> bool:
    """
    Removes a model, returning a bool depending on the status.
    """
    # Ensuring the model is a valid model
    if model in await listModels():
        ollama.delete(model)
        return True
    return False

def running() -> list:
    return ollama.ps()['models']



class History:
    """
    History class maintains a dictionary of chat histories.

    Each chat is identified by a key 'chat-{chat_id}' and stores a list of message dicts.

    Way of storing:
        {"chat-0":[ {"role":"user","content":"content"}, {"role":"assistant":"content":"content"}, {etc...}]}
    """
    def __init__(self, file="chats.json") -> None:
        self.value = {}
        self.loadHistory(file)

    def add(self, addition: list[dict[str, str]], chat: int) -> bool:
        """
        Adds to the history.

        Structure for storing: [ {"role":"user", "content":"Example from User"}, {"role":"assistant", "content":"Example from Assistant"} ]

        The chat parameter is for what "chat" is being saved to.

        Note: If chat doesn't exist, it will be created.
        """
        # Validate each message in addition
        for i in addition:
            if len(i) != 2:
                return False
            if i["role"] not in ["user", "assistant"]:
                return False
            if "content" not in i:
                return False
        chat_key = f"chat-{chat}"
        if chat_key not in self.value:
            self.value[chat_key] = []
            self.value[chat_key].append(addition)
        else:
            self.value[chat_key].append(addition)
        return True

    def remove(self, remove: int, chat: int) -> bool:
        """
        Removes a message at index 'remove' from the chat history for the given chat.

        Returns True if successful, False otherwise.
        """
        chat_key = f"chat-{chat}"
        if chat_key not in self.value:
            return False
        if remove < 0 or remove >= len(self.value[chat_key]):
            return False
        del self.value[chat_key][remove]
        return True

    def edit(self, item: int, newVal: str, chat: int, role:str) -> bool:
        """
        Edits the 'content' of a message at index 'item' in the chat history for the given chat.

        Optionally checks for role match if provided.

        Returns True if successful, False otherwise.

        """
        chat_key = f"chat-{chat}"
        if chat_key not in self.value:
            return False
        if item < 0 or item >= len(self.value[chat_key]):
            return False
        if role and self.value[chat_key][item]["role"] != role:
            return False
        self.value[chat_key][item]["content"] = newVal
        return True

    def getHistory(self, chat: int) -> list[dict[str,str]]:
        """
        Returns the chat history (list of messages) for the given chat.

        Returns an empty list if chat does not exist.
        """
        chat_key = f"chat-{chat}"
        return self.value.get(chat_key, [])
    
    def saveHistory(self, file:str) -> bool:
        """
        Saves the current history to a specific file, given that it is possible.

        If it can't write, False. True otherwise.
        """
        saveFile = open(file, "w")
        if saveFile.writable():
            saveFile.write(json.dumps(self.value))
            return True
        return False
        
    def loadHistory(self, file) -> bool:
        """
        Loads history from a given file.

        If file exists and can be loaded, loads file and returns `True`. Otherwise, returns `False`.

        Warning: This will delete current contents
        """
        
        loadFile = open(file, "r")
        if loadFile.readable():
            contents = loadFile.read()
            if len(contents) > 2:
                self.value = json.loads(contents)
                loadFile.close()
                return True
        
        loadFile.close()
        return False
        






# Pre-made for those who don't want to define the history variable themselves.
__hist = History()
async def sendPrompt(model:str, prompt:str, chat:int) -> str:
    """
    Sends the prompt to a model.

    Autosaves to history to chat.
    """
    if (type(model) == None or type(prompt) == None):
        return ""
    response: ollama.ChatResponse = ollama.chat(model=model, messages=__hist.getHistory(chat))
    if type(response.message.content) == str:
         __hist.add([{"role":"user","content":prompt},{"role":"assistant","content":response.message.content}],chat)
    if type(response.message.content) == str:
        return response.message.content
    return ""

def removeHistory(item:int, chat:int) -> bool:
    """
    Removes a piece of history, provided that the item exists.
    """
    return __hist.remove(item, chat)
    
def editHistory(item:int, newValue:str, chat:int, role:str) -> bool:
    """
    Edits a piece of history, provided that it exists.

    If it succeeds, then it'll return True. False otherwise.
    """
    return __hist.edit(item,newValue,chat,role)
    
def getHistory(chat:int) -> list[dict[str,str]]:
    """
    Returns the history of a given chat. If the chat doesn't exist, returns empty list.
    """
    return __hist.getHistory(chat)

def saveHistory(file:str) -> bool:
    return __hist.saveHistory(file)

def loadHistory(file:str) -> Exception|bool:
    return __hist.loadHistory(file)
