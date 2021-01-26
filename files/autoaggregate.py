import yaml
from pprint import pprint
import re

exclude_list = ["ENV", "ONLY"]

########  repos #########
with open(r"repos.yaml") as file:
    a = yaml.load_all(file, Loader=yaml.FullLoader)
    for doc in a:
        print(doc.keys())
        global repos_dict
        repos_dict = doc

#########  addons #########
with open(r"addons.yaml") as file:
    a = yaml.load_all(file, Loader=yaml.FullLoader)
    for doc in a:
        if "ENV" in doc.keys():
            repoName = doc["ENV"]["DEFAULT_REPO_PATTERN"]
        else:
            repoName = "https://github.com/OCA/{}.git"
        print(doc.keys())
        for repo in doc.keys():
            if repo not in repos_dict.keys() and repo not in exclude_list:

                repos_dict["./" + repo] = {
                    "defaults": {
                        "depth": "$DEPTH_DEFAULT",
                    },
                    "merges": ["ocb $ODOO_VERSION"],
                    "remotes": {"ocb": repoName.format(repo)},
                    "target": "ocb $ODOO_VERSION",
                }

with open("repos.yml", "w") as outfile:
    yaml.dump(repos_dict, outfile, default_flow_style=False)
