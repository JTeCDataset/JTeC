# JTeC: A Large Collection of Java Test Classes for Test Code Analysis and Processing [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2878368.svg)](http://doi.org/10.5281/zenodo.2878368) 

This repository is the companion for the dataset: 
> F. Corò,  R.  Verdecchia,  E.  Cruciani,  B.  Miranda,  and  A.  Bertolino, "JTeC:  A  large  collection  of  Java  test  classes  for test  code  analysisand  processing". [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2878368.svg)](http://doi.org/10.5281/zenodo.2878368) 
 
It contains the implementation of all the steps required in order generate our dataset, including: (i) filtering of GitHub repositories, (ii) Java repository selection, (iii) test classes identification, (iv) repository selection, and (v) local storage of test classes.

Moreover it contains the quality filter script [quality_filter.py](https://github.com/MSR19-JTeC/JTeC/blob/master/python3/quality_filter.py) that cleans the dataset according to some quality criteria defined by the user.

You can cite the dataset in BibTeX via 
~~~
@misc{coro_federico_2019_2878368,
  author       = {Corò, Federico and
                  Verdecchia, Roberto and
                  Cruciani, Emilio and
                  Miranda, Breno and
                  Bertolino, Antonia},
  title        = {{JTeC: A Large Collection of Java Test Classes 
                   forTest Code Analysis and Processing}},
  month        = may,
  year         = 2019,
  note         = {{Companion page for the JTeC dataset at 
                   https://github.com/JTeCDataset/JTeC}},
  doi          = {10.5281/zenodo.2878368},
  url          = {https://doi.org/10.5281/zenodo.2878368}
}
~~~

## Dataset replication

In order to replicate the dataset follow these steps:

1. Clone the repository 
   - `git clone https://github.com/MSR19-JTeC/JTeC`
 
2. Make sure to satisfy the following requirements:
    * Have Python 3.0+ installed
    * Possess a valid GitHub username and personal GitHub access token
    
3. Modify the file `token.txt` by changing the fields to your personal GitHub username and access token
   
4. Execute the script which launches in sequential order the JTeC generation steps (see Section "JTeC generation steps")
    - `sh JTeC_generator.sh`

5. Run the quality filter script via `python3 quality_filter.py`


## JTeC generation steps

The steps required in order to generate the dataset are implemented in the following 4 scripts, which have to be executed sequentially in the order given below. A brief description of the scripts is provided below:

1. [repository_filtering.py](https://github.com/MSR19-JTeC/JTeC/blob/master/repository_filtering.py) - Script generating an index of GitHub public repositories (Step 1). <br> The final output of this script consists of a local .csv file containing for each public repository indexed the following fields: _repositoryID_, _username of repository creator_, _name of the repository_, and _programming languages associated to the repository_

2. [selection_test_count.py](https://github.com/MSR19-JTeC/JTeC/blob/master/selection_test_count.py) - Script selecting Java repositories (Step 2) and identifying test classes of the selected repositories (Step 3). This script takes as parameter the programming language to be considered for the generation of the dataset, e.g. `selection_test_count.py Java`.<br>
The final output of this script consists of a local .csv file containing the following information: _user_, _repository_, _id_, _hash_, _date_, _n_tests_, _fork_id_.

3. [select.py](https://github.com/MSR19-JTeC/JTeC/blob/master/selection_test_count.py) - Script selecting among each forked project either the original or forked project according to which one contains more test classes (Step 4). <br>
The final output of this script consists of a local .csv file containing the following information: _user_, _repository_, _id_, _hash_, _date_, _n_tests_, _fork_id_.

4. [download_tests.py](https://github.com/MSR19-JTeC/JTeC/blob/master/download_tests.py) - Script downloading the test classes of the repositories selected by `select.py` (Step 5). <br>
This script takes as input the list of repositories for which we want to download the test classes and create the dataset. <br>
The final output of this script is: (i) the totality of the source code of the identified test classes, and (ii) a .csv file containing the following fields: _user_, _repository_, _id_,_fork_id_,_hash_, _date_, _n_tests_, _SLOC_, _size_

5. [quality_filter.py](https://github.com/MSR19-JTeC/JTeC/blob/master/quality_filter.py) - Script cleaning the raw dataset obtained after previous step. Next section describes the script more in detail.


## JTeC Quality Filter

JTeC provides a simple method to trim the dataset in order to make it satisfy some quality criteria, e.g., test suite size measured by number of test cases in the test suite.
The criteria can be customized by simply changing a configuration file.

### Configuration file
Set configuration file [config.json](https://github.com/MSR19-JTeC/JTeC/blob/master/config.json)

- `BOOL_TS_Clone`: Copy Output Dataset In New Folder (Values: true, false)
- `BOOL_TS_Index`: Create Test Suite Index (Values: true, false)
- `BOOL_TS_Original`: Select Original Projects (Values: true, false)
- `BOOL_TS_Fork`: Select Fork Projects (Values: true, false)
- `MIN_TS_Year`: Lower Bound on Project's Test Suite Years Range (Values: 0,1,2,...; Unbounded: -1)
- `MAX_TS_Year`: Upper Bound on Project's Test Suite Years Range (Values: 0,1,2,...; Unbounded: -1)
- `MIN_TS_Size`: Lower Bound on Total Number of Project's Test Cases - Test Suite Size (Values: 0,1,2,...; Unbounded: -1)
- `MAX_TS_Size`: Upper Bound on Total Number of Project's Test Cases - Test Suite Size (Values: 0,1,2,...; Unbounded: -1)
- `MIN_TS_SLOCs`: Lower Bound on Total Number of SLOCs of Project's Test Suite (Values: 0,1,2,...; Unbounded: -1)
- `MAX_TS_SLOCs`: Upper Bound on Total Number of SLOCs of Project's Test Suite (Values: 0,1,2,...; Unbounded: -1)
- `MIN_TS_Bytes`: Lower Bound on Total Number of Bytes of Project's Test Suite (Values: 0,1,2,...; Unbounded: -1)	
- `MAX_TS_Bytes`: Upper Bound on Total Number of Bytes of Project's Test Suite (Values: 0,1,2,...; Unbounded: -1)


### Quality Filter Script
After having changed the configuration file, run the quality filter script [quality_filter.py](https://github.com/MSR19-JTeC/JTeC/blob/master/python3/quality_filter.py) via `python3 quality_filter.py`


## Utility files

In addition to the scripts described in Section "JTeC generation steps", the dataset generation process makes use of two utility scripts and one utility file, namely:
* [request_manager.py](https://github.com/MSR19-JTeC/JTeC/blob/master/request_manager.py) - Script managing all GitHub requests and handling possible error arising at request time, returning eventually a specific error-number to the script that first sent the request.
* [credentials.py](https://github.com/MSR19-JTeC/JTeC/blob/master/credentials.py) - Script loading from the file `tokens.txt` the username and access tokens required to query the GitHub API.
* [tokens.txt](https://github.com/MSR19-JTeC/JTeC/blob/master/tokens.txt) - Text file containing the GitHub username and personal GitHub access token.
