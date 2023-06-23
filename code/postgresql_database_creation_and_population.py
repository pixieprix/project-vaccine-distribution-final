from pathlib import Path
import psycopg2
import pandas as pd
import json
import datetime

#------------------------------------
# Establish Connection
#------------------------------------

def connect(credentials, verbose = False):
   try:
      connection = psycopg2.connect(
         database=credentials['database'],
         user=credentials['user'],
         password=credentials['password'], 
         host=credentials['host'],
         port=credentials['port']
      )
      connection.autocommit = True
      cursor = connection.cursor()
      if (verbose):
         print("PostgreSQL server information")
         print(connection.get_dsn_parameters(), "\n")
         cursor.execute("SELECT version();")
         record = cursor.fetchone()
         print("You are connected to:", record, "\n")
      return connection, cursor

   except Exception as e:
      print("Exception occured!")
      print(f"{type(e).__name__}: {e}")

#------------------------------------
# Run SQL File
#------------------------------------

def run_sql_from_file(sql_file, psql_conn):
    '''
	read a SQL file with multiple stmts and process it
	adapted from an idea by JF Santos
	Note: not really needed when using dataframes.
    '''
    sql_command = ''
    for line in sql_file:
        #if line.startswith('VALUES'):        
     # Ignore commented lines
        if not line.startswith('--') and line.strip('\n'):        
        # Append line to the command string, prefix with space
           sql_command +=  ' ' + line.strip('\n')
           #sql_command = ' ' + sql_command + line.strip('\n')
        # If the command string ends with ';', it is a full statement
        if sql_command.endswith(';'):
            # Try to execute statement and commit it
            try:
                psql_conn.execute(str(sql_command))
                #psql_conn.commit()
            # Assert in case of error
            except Exception as e:
                print(e)
                print('Error at command:'+sql_command + ".")
                ret_ =  False
            # Finally, clear command string
            finally:
                sql_command = ''           
                ret_ = True
    return ret_

if __name__ == "__main__":

    #------------------------------------
    # Read Credential and Connect
    #------------------------------------

    # course db
    with open('course_credentials.json', 'r') as f:
        credentials = json.load(f)

    connection, cursor = connect(credentials, verbose=True)

    #------------------------------------
    # Table Creation
    #------------------------------------

    repo_location = (Path(__file__).absolute().parent.parent)
    sql_file1  = open(f"{repo_location}/code/create_base_tables.sql")
    run_sql_from_file (sql_file1, cursor)

    #------------------------------------
    # Data Insertion Preparation
    #------------------------------------

    output_file = f"{repo_location}/code/populate_tables.sql"
    output_file_handle = open(output_file, "w")
    excel_file_path = f"{repo_location}/data/vaccine-distribution-data.xlsx"

    #------------------------------------
    # VaccineType
    #------------------------------------

    table_name = "VaccineType"
    output_file_handle.write(f"-- Populate {table_name} table\n")
    df = pd.read_excel(excel_file_path, table_name)
    for idx, row in df.iterrows():
        buffer = f"INSERT INTO {table_name} VALUES (" + \
                    f"'{str(row['ID'])}'" + ", " +\
                    f"'{str(row['name'])}'" + ", " + \
                    str(row['doses']) + ", " + \
                    str(row['tempMin']) + ", " + \
                    str(row['tempMax']) + ") ON CONFLICT DO NOTHING;"
        output_file_handle.write(buffer + "\n")
    output_file_handle.write("\n\n")

    #------------------------------------
    # Manufacturer
    #------------------------------------

    table_name = "Manufacturer"
    output_file_handle.write(f"-- Populate {table_name} table\n")
    df = pd.read_excel(excel_file_path, table_name)
    for idx, row in df.iterrows():
        buffer = f"INSERT INTO {table_name} VALUES (" + \
                    f"'{str(row['ID'])}'" + ", " +\
                    f"'{str(row['country'])}'" + ", " + \
                    f"'{str(row['phone'])}'" + ", " + \
                    f"'{str(row['vaccine'])}'" + ") ON CONFLICT DO NOTHING;"
        output_file_handle.write(buffer + "\n")
    output_file_handle.write("\n\n")

    #------------------------------------
    # VaccinationStations
    #------------------------------------

    table_name = "VaccinationStations"
    output_file_handle.write(f"-- Populate {table_name} table\n")
    df = pd.read_excel(excel_file_path, table_name)
    for idx, row in df.iterrows():
        buffer = f"INSERT INTO {table_name} VALUES (" + \
                    f"'{str(row['name'])}'" + ", " \
                    f"'{str(row['address'])}'" + ", " + \
                    f"'{str(row['phone'])}'" + ") ON CONFLICT DO NOTHING;"
        output_file_handle.write(buffer + "\n")
    output_file_handle.write("\n\n")

    #------------------------------------
    # VaccineBatch
    #------------------------------------

    table_name = "VaccineBatch"
    output_file_handle.write(f"-- Populate {table_name} table\n")
    df = pd.read_excel(excel_file_path, table_name)
    for idx, row in df.iterrows():
        buffer = f"INSERT INTO {table_name} VALUES (" + \
                    f"'{str(row['batchID'])}'" + ", " \
                    f"{str(row['amount'])}" + ", " \
                    f"'{str(row['type'])}'" + ", " \
                    f"'{str(row['manufacturer'])}'" + ", " \
                    f"'{str(row['manufDate'])}'" + ", " + \
                    f"'{str(row['expiration'])}'" + ", " + \
                    f"'{str(row['location'])}'" + ") ON CONFLICT DO NOTHING;"
        output_file_handle.write(buffer + "\n")
    output_file_handle.write("\n\n")

    #------------------------------------
    # Transportation log
    #------------------------------------

    table_name = "Transportation log"
    output_file_handle.write(f"-- Populate {table_name} table\n")
    df = pd.read_excel(excel_file_path, table_name)
    for idx, row in df.iterrows():
        buffer = f"INSERT INTO TransportationLog VALUES (" + \
                    f"'{str(row['batchID'])}'" + ", " \
                    f"'{str(row['arrival'])}'" + ", " \
                    f"'{str(row['departure '])}'" + ", " \
                    f"'{str(row['dateArr'])}'" + ", " \
                    f"'{str(row['dateDep'])}'" + ") ON CONFLICT DO NOTHING;"
        output_file_handle.write(buffer + "\n")
    output_file_handle.write("\n\n")

    #------------------------------------
    # StaffMembers
    #------------------------------------

    table_name = "StaffMembers"
    output_file_handle.write(f"-- Populate {table_name} table\n")
    df = pd.read_excel(excel_file_path, table_name)
    for idx, row in df.iterrows():
        buffer = f"INSERT INTO Staffmembers VALUES (" + \
                    f"'{str(row['social security number'])}'" + ", " \
                    f"'{str(row['name'])}'" + ", " \
                    f"'{str(row['date of birth'])}'" + ", " \
                    f"'{str(row['phone'])}'" + ", " \
                    f"'{str(row['role'])}'" + ", " \
                    f"'{str(row['vaccination status'])}'" + ", " \
                    f"'{str(row['hospital'])}'" + ") ON CONFLICT DO NOTHING;"
        output_file_handle.write(buffer + "\n")
    output_file_handle.write("\n\n")

    #------------------------------------
    # Shifts
    #------------------------------------

    table_name = "Shifts"
    output_file_handle.write(f"-- Populate {table_name} table\n")
    df = pd.read_excel(excel_file_path, table_name)
    weekday_to_num = {
        "Sunday"    : 0,
        "Monday"    : 1,
        "Tuesday"   : 2,
        "Wednesday" : 3,
        "Thursday"  : 4,
        "Friday"    : 5,
        "Saturday"  : 6,
    }
    for idx, row in df.iterrows():
        weekday = row['weekday']
        buffer = f"INSERT INTO {table_name} VALUES (" + \
                    f"'{str(row['station'])}'" + ", " \
                    f"{weekday_to_num[row['weekday']]}" + ", " \
                    f"'{str(row['worker'])}'" + ") ON CONFLICT DO NOTHING;"
        output_file_handle.write(buffer + "\n")
    output_file_handle.write("\n\n")

    #------------------------------------
    # Vaccinations
    #------------------------------------

    table_name = "Vaccinations"
    output_file_handle.write(f"-- Populate {table_name} table\n")
    df = pd.read_excel(excel_file_path, table_name)
    for idx, row in df.iterrows():
        buffer = f"INSERT INTO {table_name} VALUES (" + \
                    f"'{str(row['date'])}'" + ", " \
                    f"'{str(row['location '])}'" + ", " \
                    f"'{str(row['batchID'])}'" + ") ON CONFLICT DO NOTHING;"
        output_file_handle.write(buffer + "\n")
    output_file_handle.write("\n\n")

    #------------------------------------
    # Patients
    #------------------------------------

    table_name = "Patients"
    output_file_handle.write(f"-- Populate {table_name} table\n")
    df = pd.read_excel(excel_file_path, table_name)
    for idx, row in df.iterrows():
        formatted_name = str(row['name']).replace("'","''")
        buffer = f"INSERT INTO {table_name} VALUES (" + \
                    f"'{str(row['ssNo'])}'" + ", " \
                    f"'{formatted_name}'" + ", " \
                    f"'{str(row['date of birth'])}'" + ", " \
                    f"'{str(row['gender'])}'" + ") ON CONFLICT DO NOTHING;"
        output_file_handle.write(buffer + "\n")
    output_file_handle.write("\n\n")

    #------------------------------------
    # VaccinePatients
    #------------------------------------

    table_name = "VaccinePatients"
    output_file_handle.write(f"-- Populate {table_name} table\n")
    df = pd.read_excel(excel_file_path, table_name)
    for idx, row in df.iterrows():
        buffer = f"INSERT INTO {table_name} VALUES (" + \
                    f"'{str(row['date'])}'" + ", " \
                    f"'{str(row['location'])}'" + ", " \
                    f"'{str(row['patientSsNo'])}'" + ") ON CONFLICT DO NOTHING;"
        output_file_handle.write(buffer + "\n")
    output_file_handle.write("\n\n")

    #------------------------------------
    # Symptoms
    #------------------------------------

    table_name = "Symptoms"
    output_file_handle.write(f"-- Populate {table_name} table\n")
    df = pd.read_excel(excel_file_path, table_name)
    for idx, row in df.iterrows():
        buffer = f"INSERT INTO {table_name} VALUES (" + \
                    f"'{str(row['name'])}'" + ", " \
                    f"'{str(row['criticality'])}'" + ") ON CONFLICT DO NOTHING;"
        output_file_handle.write(buffer + "\n")
    output_file_handle.write("\n\n")

    #------------------------------------
    # Diagnosis
    #------------------------------------

    table_name = "Diagnosis"
    output_file_handle.write(f"-- Populate {table_name} table\n")
    df = pd.read_excel(excel_file_path, table_name)
    for idx, row in df.iterrows():
        format_date = f"'{row['date']}'" if type(row['date']) == datetime.datetime else 'NULL'
        buffer = f"INSERT INTO {table_name} (patient, symptom, diagnosis_date) VALUES (" + \
                    f"'{str(row['patient'])}'" + ", " \
                    f"'{str(row['symptom'])}'" + ", " \
                    f"{format_date}" + ") ON CONFLICT DO NOTHING;"
        output_file_handle.write(buffer + "\n")
    output_file_handle.write("\n\n")

    #------------------------------------
    # Data Insertion
    #------------------------------------

    output_file_handle.close()#close the file so the writing buffer is flushed
    sql_file1  = open('./populate_tables.sql')
    run_sql_from_file (sql_file1, cursor)

    #------------------------------------
    # Close Connection
    #------------------------------------

    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")