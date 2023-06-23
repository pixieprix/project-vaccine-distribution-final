import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Implementation", page_icon="🔧")


st.markdown("# Implementation")

st.header("Ensuring Boyce - Codd Normal Form")

st.markdown("""After deciding on the relational schemas, the first thing to do is to ensure Boyce-Codd Normal Form (BCNF) for the relations to avoid redundancies that can cause anomalies in the system. Since this database is simple, it is relatively easy to check for BCNF as most of the relations have either one or all of the attributes forming the primary key. The one remaining Vaccinations relation that does not exhibit this property is easy to be checked.

Assuming that the relations are more complex, the workflow to check for BCNF follows:

- Find a tool designated for checking BCNF (keyword: BCNF solver, BCNF normalisation tool, etc…). Either you can find them by Googling, and they might come in convenient forms like interactive websites or handy python scripts. Professional database schema tools are likely to provide such a feature, but our group has not tried any of them.
- Input your relation schema (one relation at a time), as well as all the functional dependencies. The tool should state whether the current relation is in BCNF form.
- If the current relation is not in BCNF form, break it down into smaller relations and try the previous step again.
""")

st.header("Scripting")

st.markdown("""

We used python to parse the given excel, create, then populate the corresponding relations. In the end we have:

- One python script to create the database tables, as well as populate them.
- One SQL file to create the tables in the database.
- One python file to answer the questions in part 2 of the project.
- One jupyter notebook to answer the questions in part 3 of the projects.

Here is a summary of our workflow:

The first step is to make experiments in a jupyter notebook. Jupyter notebook offers an advantage over .py files by allowing "partial file execution.". This means you can select specific code cells to execute, making the process of trial and error much less troublesome. This feature, coupled with the ability to document using markdown, is why data-related work often favours notebooks over plain Python scripts. In cases where the cell is expected to modify the database, we utilise DBeaver to manually verify the outcome.

Once we are satisfied with the notebook, we proceed to convert it into a Python script. The Jupyter notebook extension provides a tool for this conversion. The resulting script is then executed multiple times on group members’ machines. Between each testing iteration, the database is deleted. To validate the data process, we compare the tables in the database to the corresponding rows in the Excel sheets, as the database's relations closely resemble those of the Excel sheets.
""")

st.header("Brief User Manual")

st.markdown("""
The project deliverable package specifically contains these following files:
- The SQL file used to create the tables in our database: create\_base\_tables.sql
- The python file used to connect to the database, import, clean and populate data into the tables, and execute sql queries:
postgresql_database_creation_and_population.py
- The .txt file containing necessary dependencies: requirements.txt
- The .json file storing our credentials separately for login purposes: course_credentials.json
- Instructions to run the Python script are as following:
    1. Install dependencies in - requirements.txt. We added openpyxl as a dependency to read the Excel file with sample data and tabulate for display.
    2. Update Database credentials - course_credentials.json
    3. Once the user has the virtual environment and the right credentials, the following command can be executed in the terminal to run the python script:

""")

st.code('''python postgresql_database_creation_and_population.py''', language="python", line_numbers=False)