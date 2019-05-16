import json
import os.path
import shutil


if __name__ == '__main__':
    config_file = "config.json"
    JTeC_CSV_Raw = "JTeC.csv"
    base_path = os.path.join("JTeC")
    base_new_path = os.path.join("JTeC-Clean")

    if not os.path.isfile(config_file):
        print("Configuration File Missing!")
        exit()

    if not os.path.isfile(JTeC_CSV_Raw):
        print("Original JTeC Index Missing!")
        exit()

    if not os.path.exists(base_path):
        print("Original JTeC Dataset Missing!")
        exit()

    # Read configuration file
    with open(config_file) as file_in:
        nocomment = "".join(line for line in file_in if "//" not in line)
        config = json.loads(nocomment)

    # transform -1 in infty
    for k, v in config.items():
        if "MAX" in k and v < 0:
            config[k] = float("Inf")

    print("JTeC CONFIGURATION: ", end="")
    print(json.dumps(config, indent=1, sort_keys=True))
    print()

    # filter projects
    JTeC_CSV = ""
    number_of_repo, number_of_test_cases, total_size, number_of_SLOCs = 0, 0, 0, 0
    min_year, max_year = float("Inf"), -float("Inf")
    with open(JTeC_CSV_Raw) as file_in:
        h = next(file_in)
        for line in file_in:
            (repo_id, user, repo, fork_id, commit, commit_date,
                n_tests, size, SLOCs) = (x.strip() for x in line.split(","))
            n_tests, size, SLOCs = int(n_tests), int(size), int(SLOCs)
            year = int(commit_date[:4])
            if (((config["BOOL_TS_Original"] and fork_id == "-") or
                    (config["BOOL_TS_Fork"] and fork_id != "-")) and
                config["MIN_TS_Year"] <= year <= config["MAX_TS_Year"] and
                config["MIN_TS_Size"] <= n_tests <= config["MAX_TS_Size"] and
                config["MIN_TS_Bytes"] <= size <= config["MAX_TS_Bytes"] and
                config["MIN_TS_SLOCs"] <= SLOCs <= config["MAX_TS_SLOCs"]):

                JTeC_CSV += line
                number_of_repo += 1
                number_of_test_cases += n_tests
                total_size += size
                number_of_SLOCs += SLOCs
                min_year = year if year < min_year else min_year
                max_year = year if year > max_year else max_year

    # write JTeC index
    if config["BOOL_TS_Index"]:
        with open("JTeC-Clean.csv", "w") as file_out:
            file_out.write(h)
            file_out.write(JTeC_CSV)

    # clone JTeC
    if config["BOOL_TS_Clone"]:
        if os.path.exists(base_new_path):
            shutil.rmtree(base_new_path)
        try:
            for line in JTeC_CSV.strip().split("\n"):
                (repo_id, user, repo, fork_id, commit, commit_date,
                    n_tests, size, SLOCs) = (x.strip() for x in line.split(","))
                path = os.path.join(base_path, user, repo)
                new_path = os.path.join(base_new_path, user, repo)
                shutil.copytree(path, new_path)
        except:
            pass

    # print JTeC summary
    print("JTeC DATASET SUMMARY: ")
    print(" - Number of Projects:", number_of_repo)
    print(" - Total Number of TestCases:", number_of_test_cases)
    print(" - Total Number of SLOCs:", number_of_SLOCs)
    print(" - Total Size in Bytes:", total_size)
    print(" - Years Range:", min_year, "-", max_year)
