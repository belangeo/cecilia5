import os
import xmlrpc.client as xmlrpclib

PRESETS_DELIMITER = "####################################\n" \
                    "##### Cecilia reserved section #####\n" \
                    "#### Presets saved from the app ####\n" \
                    "####################################\n"

root = "/home/olivier/git/cecilia5/Resources/modules/"
folders = os.listdir(root)

presets_folder = "/home/olivier/.cecilia5/presets/"

for folder in folders:
    files = os.listdir(os.path.join(root, folder))
    for file in files:
        mylocals = {}
        rewrite = False
        with open(os.path.join(root, folder, file), "r") as f:
            text = f.read()
            if PRESETS_DELIMITER in text:
                rewrite = True
                newtext = text[:text.find(PRESETS_DELIMITER) - 1]
                text = text[text.find(PRESETS_DELIMITER) + len(PRESETS_DELIMITER) + 1:]
                if text.strip() == "":
                    print("No presets...")
                    continue
                exec(text, globals(), mylocals)

                fileName = os.path.splitext(file)[0]
                if not os.path.isdir(os.path.join(presets_folder, fileName)):
                    os.mkdir(os.path.join(presets_folder, fileName))

                for preset in mylocals["CECILIA_PRESETS"]:
                    for key in list(mylocals["CECILIA_PRESETS"][preset]["plugins"]):
                        mylocals["CECILIA_PRESETS"][preset]["plugins"][str(key)] = mylocals["CECILIA_PRESETS"][preset]["plugins"][key]
                        del mylocals["CECILIA_PRESETS"][preset]["plugins"][key]
                    msg = xmlrpclib.dumps((mylocals["CECILIA_PRESETS"][preset], ), allow_none=True)
                    with open(os.path.join(presets_folder, fileName, preset), "w") as fw:
                        fw.write(msg)
        if rewrite:
            with open(os.path.join(root, folder, file), "w") as f:
                f.write(newtext)
