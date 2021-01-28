from sys import argv
from os import symlink
import yaml
import re
from collections import Iterable


exclude_list = ["ENV", "ONLY"]
addons = []
auto_addons_path = "/opt/odoo/auto/addons/"
custom_addons_path = "/opt/odoo/custom/src/"

######## OCA addons #########
# not need symbolyc links? even if it has aggregation?

######## custom addons #########
with open(r"addons.yaml") as file:
    docs = yaml.load_all(file, Loader=yaml.FullLoader)
    for doc in docs:
        addons.append(
            [doc[key] if key not in exclude_list else ["exclude"] for key in doc.keys()]
        )

        for repo in doc.keys():
            if repo not in exclude_list:
                for addon in doc[repo]:
                    src = custom_addons_path + repo + "/" + addon
                    dest = auto_addons_path + addon
                    # print("src:--{>}", src)
                    # print("dest:--{>}", dest)
                    try:
                        symlink(src, dest)
                    except Exception as error:
                        print(error)
            else:
                continue
