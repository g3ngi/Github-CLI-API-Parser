import json
import subprocess
import sys

class Commit:
    def __init__(self, name, commit_message, pull_message=None):
        self.name = name
        self.commit_message = commit_message
        self.pull_message = pull_message
    
    def to_dict(self):
        return {
            "name" : self.name,
            "commit_message" : self.commit_message,
            "pull_message" : self.pull_message
        }

json_data = []
commits = []

def requestData(user, repo):
    response = subprocess.run(
        f"gh api repos/{user}/{repo}/commits",
        capture_output=True,
        shell=True,
        text=True
    )

    raw_output = response.stdout

    jq_response = subprocess.run(
        "jq '[.[] | {name: .commit.author.name, message: .commit.message}]'",
        input=raw_output,
        capture_output=True,
        shell=True,
        text=True
    )

    json_data = json.loads(jq_response.stdout)
    return json_data

def sendData(data):
    for i in range(5):
        name = data[i]["name"]

        if data[i]["message"].find("Merge") >= 0:
            commit_message = data[i]["message"][44:]
            pull_message = data[i]["message"][:42]
        
        else:
            commit_message = data[i]["message"]
            pull_message = None
        
        parsed_data = Commit(name, commit_message, pull_message)
        commits.append(parsed_data.to_dict())

    print(json.dumps(commits))

def main():
    user = sys.argv[1]
    repo = sys.argv[2]
    data = requestData(user, repo)
    sendData(data)

if __name__ == "__main__":
    main()



