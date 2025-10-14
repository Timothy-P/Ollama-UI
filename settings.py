"""
A relatively simple way of making, editing, or retrieving settings.

Supports JSON and CSS files. Automatically formats to the file's format.
"""

import json
class Settings():
    def __init__(self, file:str = "static/style.css") -> None:
        self.value:dict[str,dict[str,str]] = {}
        self.loadSettings(file)

    def loadSettings(self, file:str) -> bool:
        """
        Loads a file containing the desired settings.
        Supports both JSON and CSS files.
        """
        # This was modified using AI. Most of this is my doing.

        try:
            # If JSON, loads
            if file.endswith('.json'):
                with open(file, "r") as sett:
                    self.value = json.load(sett)
            # If CSS, translates
            elif file.endswith('.css'):
                JSON = self.__css_to_json(file)
                if type(JSON) == dict:
                    self.value = JSON
            # If neither, doesn't do anything
            else:
                print(f"Unsupported file type: {file}")
                return False
        # If error, tries to load CSS default
        # If fails, returns exception and gives up
        except Exception as e:
            print(f"Failed to load given file. Loading default CSS file.\n     Exception: {e}")
            #try:
            JSON = self.__css_to_json("static/style.css")
            if type(JSON) == dict:
                self.value = JSON
            #except Exception as e:
                #print(f"Failed to load default CSS file. Returning exception.\n    Exception: {e}\n")
                #return False
        return True

    def saveSettings(self, file:str) -> bool:
        """
        Saves settings to the desired file.
        Supports both JSON and CSS files.
        """
        # This was modified using AI. Most of this is my doing.

        try:
            # Check if JSON
            if file.endswith('.json'):
                # Opens file
                with open(file, "w") as sett:
                    if sett.writable():
                        json.dump(self.value, sett, indent=4)
            # Check if CSS
            elif file.endswith('.css'):
                # What was it thinking????
                with open(file, "w") as css:
                    css.write(self.__json_to_css(self.value))
                return True
            else:
                print(f"Unsupported file type: {file}")
                return False
            return True
        except Exception as e:
            print(f"Failed to save settings: {e}")
            return False
    def __css_to_json(self, cssFile: str) -> dict[str,dict[str,str]]|bool:
        """
        Parses a CSS file and returns a dict of CSS properties.
        """

        with open(cssFile, "r") as file:
            if file.readable():
                lineCount:int = sum(1 for _ in file)
                file.seek(0)
                i:int = 0
                # Keys and values for return
                key:str = ""
                values:dict[str,str] = {}
                # Final return value
                final:dict[str,dict[str,str]] = {}
                # File contents
                commentCheck:bool = True
                while i < lineCount:
                    # Increment to avoid inf loop.
                    i += 1

                    line = file.readline()
                    # Set commentCheck to true if "/*" has been used
                    if bool(line.find("/*")+1): commentCheck = False
                    # Set commentCheck to false if "*/" has been used
                    if bool(line.find("*/")+1): commentCheck = True

                    if line != "\n" and commentCheck and not line.find("/*")+1 and not line.find("*/")+1:
                        
                        # Getting the key
                        if line.find("{") != -1:
                            key = line[0:line.find("{")-1]

                        # Getting the value(s)
                        elif line.find("}") == -1:
                            # The line without the indentation and line split.
                            cutLine = line.replace("  ", "").replace("\n", "").split(":")
                            # Causes index error?

                            values[cutLine[0]] = cutLine[1]

                        # Putting it in the final
                        else:
                            # Set the values
                            final[key] = values.copy()
                            # Then clear for the next loop.
                            key = ""
                            values.clear()
                        # Make sure it can be toggled if both are used in a single line
                        
                # When finished with loop, return the CSS file now in JSON format.
                return final
            return False      

    def __json_to_css(self, json: dict[str,dict[str,str]]) -> str:
        """
        Takes a dict and turns it into CSS.
        """

        returnStr = ""
        for i in json.keys():
            returnStr += i+"{\\n\n"
            for f in json[i].keys():
                returnStr += f"    {f}: {json[i][f]};\\n\n"

            returnStr += "}\\n\n"
        return returnStr
    
    def editSetting(self, elm:str, setting:str, newVal:str) -> bool:
        """
        Edits a setting. Can be existing or new.
        """
        self.value[elm][setting] = newVal
        return True
    
    def rmSetting(self, elm:str, setting:str = "") -> bool:
        """
        Deletes a setting.

        If setting is deleted, True. False otherwise.
        """
        if setting != "":
            return True if self.value[elm].pop(setting,False) else False

        return True if self.value.pop(elm,False) else False
    
    def showSetting(self, elm:str = "", setting:str = "") -> str|dict[str,str]|dict[str,dict[str,str]]:
        """
        Returns setting for the specified element.

        If setting is omitted, returns all settings for specified element.
        """
        if not elm:
            return self.value
        if setting:
            return self.value[elm].get(setting, self.value[elm])
        return self.value.get(elm, self.value)