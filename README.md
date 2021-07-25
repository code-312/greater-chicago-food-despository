[![run-tests](https://github.com/Code-For-Chicago/greater-chicago-food-despository/actions/workflows/run_tests.yaml/badge.svg)](https://github.com/Code-For-Chicago/greater-chicago-food-despository/actions/workflows/run_tests.yaml)

<h1>Code for Chicago Mapping Project Backend</h1>

Data generation for an interactive map of data in Illinois. Running this project outputs JSON files that can be used by [the frontend](https://github.com/Code-For-Chicago/greater-chicago-food-despository-ui).

<h2>Getting Started</h2>

<h3>Prerequisites</h3>

1. The latest version of [Python 3.9](https://www.python.org/downloads/release/python-396/)
2. The latest version of [Git](https://git-scm.com/downloads)
3. A Census API Key, which can be obtained by filling out [this form](https://api.census.gov/data/key_signup.html)

<h3>Running for the first time</h3>

1. Ensure Python and Git are installed.
2. Create a local directory, and open a command prompt there.
3. Clone the repository with Git:
```
git clone https://github.com/Code-For-Chicago/greater-chicago-food-despository.git . 
```
5. Create a file called `.env` in the root directory. This file is ignored via the .gitignore file to avoid committing secrets.
6. Open `.env` in a text editor and add this as the contents, replacing the second part with your personal Census API key:
```
CENSUS_KEY=REPLACE_ME_WITH_CENSUS_API_KEY
```
7. Install required modules in requirements.txt
   - Mac/Linux: `pip3 install -r requirements.txt`
   - Windows: `pip install -r requirements.txt`
8. Run start script to verify your setup is correct
   - Mac/Linux: 
       - Make script executable `chmod 755 start.sh`
       - Run `start.sh` via terminal or double click
   - Windows: run `start.bat` via command line or double click
9. If the tests do not pass, check your `.env` file and your installed python package versions

<h2>Running the Project</h2>

If the start script succeeds, you can run the project with:

 - Mac/Linux: `python3 src/main.py`
 - Windows: `python src\main.py`

Running the project generates output files in the `final_jsons` folder.

To run with memory profiling:

 - Mac/Linux:
    1. Make sure the script is executable: `chmod 755 memory_profiling/run_main.sh`
    2. Run the script: `./memory_profiling/run_main.sh`
    3. View the report: `memory_profiling/memory_profile_report.txt`
 - Windows CMD/Powershell:
    1. Run the script: `.\memory_profiling\run_main.bat`
    2. View the report: `memory_profiling\memory_profile_report.txt`


<h2>Exploring the Data</h2>

After code runs, you can view the data in a Jupyter notebook at `getting_started/example.ipynb`

 - To open the notebook with VSCode, install the Python and Jupyter extensions
 - To open the notebook with JupyterLab, see [here](https://jupyter.org/install)

<h2>Running the Tests</h2>

1. To run the unit tests, run `pytest` from the root directory. 
2. Run `flake8` from the root directory to check that code style rules have been followed.
3. Run `mypy src --ignore-missing-imports` and `mypy tests --ignore-missing-imports` from the root directory to check for type errors.
4. Also see the [GitHub Actions](.github/workflows/run_tests.yaml) for the full list of tests that run in continuous integration.

<h2>Commiting changes</h2>

1. Create a new branch for your task:
```
git checkout -b branch-name
```
2. Make your local changes.
3. Check for locally modified files:
```
git status
```
4. Stage the modified files for a commit:
```
git add .
```
5. Commit to your local repository:
```
git commit -m "Your message here"
```
6. Push your local changes to the remote repository:
```
git push --set-upstream origin branch-name
```
7. Open a pull request from the Github UI using your branch