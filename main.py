import interact

# This is gonna be a doozy...
while True:
    print("1. Send prompt\n2. List models\n3. Launch menu (temporary)\n")
    try:
        usr = input(">")
        print("\n")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt triggered. Exiting...")
        exit()
    if "1" in usr:
        try:
            print("What model do you want?")
            model = input(">")
            print("Input message.")
            message = input(">")

            print(interact.sendPrompt(model, message))
        except KeyboardInterrupt:
            print("\nKeyboard interrupt triggered. Exiting...")
            exit()

    elif "2" in usr:
        response = interact.listModels()
        for i in response:
            print(i)
        print("\n")

    elif "3" in usr:
        import menu