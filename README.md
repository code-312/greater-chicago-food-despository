[![run-tests](https://github.com/Code-For-Chicago/greater-chicago-food-despository/actions/workflows/run_tests.yaml/badge.svg)](https://github.com/Code-For-Chicago/greater-chicago-food-despository/actions/workflows/run_tests.yaml)

<h1>Code for Chicago Mapping Project Backend</h1>

Data generation for an interactive map of data in Illinois. Running this project outputs JSON files that can be used by [the frontend](https://github.com/Code-For-Chicago/greater-chicago-food-despository-ui).

<h2>Getting Started</h2>

1. Obtain a Census API key [here](https://api.census.gov/data/key_signup.html)
2. Create a file called `.env` in the root directory. This file is ignored via the .gitignore file to avoid committing secrets.
3. Open `.env` in a text editor and add this as the contents, replacing the second part with your personal Census API key:
```
CENSUS_KEY=REPLACE_ME_WITH_CENSUS_API_KEY
```
4. Ensure Python is installed.
5. Install required modules in requirements.txt
   - Mac/Linux: `pip3 install -r requirements.txt`
   - Windows: `pip install -r requirements.txt`
6. Run start script to verify your setup is correct
   - Mac/Linux: 
       - Make script executable `chmod 755 start.sh`
       - Run `start.sh` via terminal or double click
   - Windows: run `start.bat` via command line or double click
7. If the tests do not pass, check your `.env` file and your installed python package versions

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

To run the tests, run `pytest` from the root directory. Also see the [GitHub Actions](.github/workflows/run_tests.yaml) for the full list of tests that run in continuous integration.
