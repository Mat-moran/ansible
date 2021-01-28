from sys import argv
import yaml
from pprint import pprint
import re

global repos_dict

if len(argv) > 1:
    tokens = True
    token_name, token_pass = argv[1], argv[2]
else:
    tokens = False


exclude_list = ["ENV", "ONLY"]

########  repos #########
with open(r"repos.yaml") as file:
    a = yaml.load_all(file, Loader=yaml.FullLoader)
    for doc in a:
        print(doc.keys())
        repos_dict = doc

#########  addons #########
with open(r"addons.yaml") as file:
    a = yaml.load_all(file, Loader=yaml.FullLoader)
    for doc in a:
        print(doc.keys())
        for repo in doc.keys():
            if repo not in repos_dict.keys() and repo not in exclude_list:
                if "ENV" in doc.keys():
                    repoName = doc["ENV"]["DEFAULT_REPO_PATTERN"]
                    if tokens:
                        repoName = repoName.format(token_name, token_pass, repo)
                    else:
                        repoName = repoName.format(repo)
                else:
                    repoName = "https://github.com/OCA/{}.git".format(repo)
                repos_dict["./" + repo] = {
                    "defaults": {
                        "depth": "$DEPTH_DEFAULT",
                    },
                    "merges": ["ocb $ODOO_VERSION"],
                    "remotes": {"ocb": repoName},
                    "target": "ocb $ODOO_VERSION",
                }

with open("repos.yaml", "w") as outfile:
    yaml.dump(repos_dict, outfile, default_flow_style=False)
