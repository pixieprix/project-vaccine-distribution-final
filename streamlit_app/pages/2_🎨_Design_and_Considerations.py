import streamlit as st
import pandas as pd
import pydeck as pdk
from PIL import Image
import os

st.set_page_config(page_title="Design and Considerations", page_icon="🎨")


st.markdown("# Design and Considerations")

st.header("Introduction")

st.markdown("""The data we receive is essentially a mock database given as an excel file, and the requirement is creating a good relational database from the given data and implementing the requested queries. This process, in other words, is designing a database according to existing data as well as accessing data correctly for a given purpose (e.g. data analysing).
This database, in practical terms, is a test double. As the given database is much smaller than a real one where there can be millions of rows, its queries can be manually checked and mistakes could be discovered before running on the real database.
""")

st.header("Assumptions")

st.markdown("""
We made the following assumptions to construct the model:

- Each Manufacturer can only make one vaccine type (and hence one vaccine id).
- Each patient can attend at most one vaccination event per day.
- For diagnosis of symptoms, each patient can visit multiple doctors on the same day, but not at the same time. This also means that only one doctor is seen per visit.
- Each Staff can only work in one hospital.
- Each Staff can be allocated multiple weekday shifts for vaccination events. However, no staff has a vaccination shift over the weekends.
- Most Staff would be assigned Vaccination duties.
- Each manufacturer, hospital, and patient has only one contact number.
- We make no assumption that phone numbers have to be unique to an entity.
- We assume each entry of the transportation log contains exactly one vaccine batch.

While the aforementioned assumptions impose certain restrictions on the database design, they are plausible when accounting for what happens in the real world. 
""")

st.header("Database Modelling")

st.subheader("UML Model")

st.markdown("""The UML diagram of the final model, along with its associated relational schema, can be found below: """)

image = Image.open('figures/UML.png')

st.image(image, caption='Sunrise by the mountains')

st.subheader("Relational Schemas")

st.markdown(""" 
The design is heavily influenced by the excel file’s format as it is convenient for the implementation, and we do not see any redundancies problem following it. We designed the database relational schemas as below: 


- VaccineType (:blue[ID], name, doses, tempMin, tempMax)
- Manufacturer (:blue[ID], country, phone, vaccine)
- VaccineBatch (:blue[batchID]>, amount, type, manufacturer, manufDate, expiration, location)
- VaccinationStations (:blue[name], address, phone)
- Transportationlog (:blue[batchID], :blue[arrival], :blue[departure], :blue[dateArr], :blue[dateDep])
- Staffmembers (:blue[social\_security\_number], name, DOB, phone, role, vaccination_status, hospital)
- Shifts (:blue[station], :blue[worker], :blue[weekday])
- Vaccinations (:blue[date], :blue[location], batchID)
- Patients (:blue[ssNo], name, DOB, gender)
- VaccinePatients (:blue[date], :blue[location], :blue[patientSsNo])
- Symptoms (:blue[name], criticality)
- Diagnosis (:blue[id], patient, symptom, date)

*Primary keys are denoted in :blue[blue]
""")