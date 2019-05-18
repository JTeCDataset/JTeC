import os
import subprocess

import credentials, request_manager

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == "__main__":
    # personal Github Account credentials
    git_username, git_access_token = credentials.load("tokens.txt")

    repo_list = "public_repositories.csv"
    base_url = "https://api.github.com/repositories?since="
    count = -1
    number_java_repo = 0
    stopping_criterion = 50000

    if not os.path.isfile(repo_list):
        with open(repo_list, "w") as file_out:
            file_out.write("{},{},{},{}\n".format("repo_id", "user", "repo", "lang"))
            last_id = 0
    else:
        for line in open(repo_list):
            repo_id, user, repo, lang = (x.strip() for x in line.split(","))
            count += 1
            if "Java" in lang.split(";"):
                number_java_repo += 1
        if count == 0:
            last_id = 0
        else:
            last_line = subprocess.check_output(["tail", "-1", repo_list]).decode("utf-8")
            last_id = int(last_line.split(",")[0].strip())

    switch_account = 0

    with open(repo_list, "a") as file_out:
        while True:
            repos_json, switch_account = request_manager.request("{}{}".format(base_url, last_id), git_username, git_access_token, switch_account)

            for repo in repos_json:
                repo_id = int(repo["id"])
                last_id = max(repo_id, last_id)

                repo_user, repo_name = repo["full_name"].split("/")

                language_url = "https://api.github.com/repos/{}/{}/languages".format(repo_user, repo_name)
                languages_data, switch_account = request_manager.request(language_url, git_username, git_access_token, switch_account)

                if type(languages_data) == int and languages_data == 0:
                    break
                else:
                    ## all used languages
                    if len(languages_data) == 0:
                        break
                    language = ";".join(languages_data.keys())
                    count += 1

                    print("#REPO: {} \t ID: {} \t {}/{} \t LANG: {}".format(count, repo_id, repo_user, repo_name, language))
                    file_out.write("{},{},{},{}\n".format(repo_id, repo_user, repo_name, language))

                    if "Java" in languages_data.keys():
                        number_java_repo += 1
                    # stopping criterion
                    if number_java_repo > stopping_criterion:
                        quit()

                    break
