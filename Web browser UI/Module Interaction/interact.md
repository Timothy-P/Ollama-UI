# interact.py
In the simplest way, `interact.py` purely does the in between of Ollama and the server.

The `History` class currently doesn't have a method to send prompts, but that'll likely be changed in a future update.

---

# History class

## Creation

The initial creation requires a file to save to. The default will be `chats.json` if not specified.

Returns `None`

## `.add` method

`addition` is the addition to the history, and `chat` is the chat to be appended to.

`addition` has to be a list containing a dictionary containing a string for the key and value.

Structure for `additon`: 
```json
[
  {"role":"user", "content":"Example from User"},
  {"role":"assistant", "content":"Example from Assistant"}
]
```

No defaults for either argument.

If the chat doesn't exist before appending, it'll be created during the operation.

Returns `True` if successful, `False` if not.

## `.remove` method

`remove` is the pair to be deleted and `chat` is the chat that'll have the removal

`remove` will be the the index in which the desired message will be deleted.

Returns `True` if successful, `False` if not.

## `.getHistory` method

`chat` is the chat to retrieve the history from.

Returns the history of the in the standard method if it exists. An empty list if it doesn't.

## `.saveHistory` method

`file` is the file to save the current history to. Can be any file type.

Returns `True` if it wrote to the file, `False` if it couldn't.

## `.loadHistory` method

`file` is the file to load history from.

Warning: It will delete any and all history currently stored. Save beforehand to avoid data loss.

Returns `True` if successfully loaded, `False` upon failure.
