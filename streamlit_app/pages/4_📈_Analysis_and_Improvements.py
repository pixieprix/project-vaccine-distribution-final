import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Analysis and Areas of Improvement", page_icon="📈")


st.markdown("# Analysis and Areas of Improvement")

st.markdown("""In this section, we analyse the database we have come up with, as well as provide a list of possible areas of improvement that could be pursued. """)

st.header("Analysis")

st.markdown("""
The data that was presented to us was rather clean – the relations to be modelled were explicitly laid out in the excel file, and there were minimal preprocessing steps that had to be taken to implement the database. For example, the excel containing the relations already had minimal redundancies (with most being in Boyce-Codd Normal Form), which meant we did not have to spend too much time on revising and/or designing the database after receiving the data. In reality, medical data is messy and it may not be so straightforward to design a database system that contains minimal redundancies, while still being accurate.

""")

st.header("Areas of Improvement")

st.markdown("""At present, many of the design choices we have made were influenced by the data we received for the database. For example, after performing some preliminary analysis, we discovered that the team of medical personnel is mutually exclusive from the set of patients we had received. Consequently, we simplified the database design and split these two groups of people into different classes: StaffMembers and Patients. Admittedly, this is not a realistic scenario as medical personnel could very well be patients. Moving forward, one area of improvement that could be made would be to take this possibility into account, which would make the database more robust and general.

In addition, when designing the database, we had made certain assumptions which were plausible under the set of data we had received. For instance, nurses were only assigned vaccination shifts at the same location, which allowed for us to represent their shift data in a rather straightforward manner. However, in the real world, it is widely known that the medical facilities are experiencing resource shortages in light of the COVID-19 pandemic – having nurses work at only one location may not accurately reflect what happens in the real world. Furthermore, it is possible for shifts to change from week-to-week. Hence, another area of improvement would be to revise the representation of the relation VaccinationShift in the database to handle the aforementioned possibilities.

During our project, we encountered an issue with SQLAlchemy's handling of transactions, resulting in a persistent lock on the database. This problem becomes more pronounced when multiple group members execute their scripts simultaneously against the same database. As a result, we were unable to modify the table as the “to_sql()” function stay endlessly during the first two questions of part three of the project. To resolve this, we need to invoke “.commit()” at the end of each code cell to end the ongoing transaction, and ensure that we close the connection at the conclusion of the notebook. Failing to release the locks can negatively impact the database's functionality and may even lead to system deadlocks.

While the current database is relatively small and optimising it for performance would not result in any significant performance boost, it is important to note that in much larger databases with numerous tables and hundreds of thousands of rows, setting up appropriate indices can greatly reduce the query time. There are numerous demonstrations on YouTube showcasing adding the correct index can result in query time reductions of up to 100 times. Although we understand the advantages of using indices, we are still unfamiliar with efficient techniques for crafting them. Optimization is a delicate art that takes time to master, and as novices, we have yet to attain that level of expertise.

Another improvement aspect can be considered is to implement triggers in the database. An SQL trigger allows us to specify SQL actions that should be executed automatically when a specific event occurs in the database. Triggers are beneficial and useful with the three most common case uses: enforcing business rules, automating tasks and maintaining database integrity. In this vaccination distribution database specifically, there are a few possible scenarios where triggers can be applied, for example:

- A trigger to ensure that the number of each patient’s vaccination entries should not exceed the number of doses required. In other words, a patient should not take more vaccine doses than needed.
- A trigger to ensure that a patient cannot attend more than one vaccination event per day.
- A trigger to ensure that a vaccination station cannot organise multiple vaccination events on one weekday. A second invalid entry should be removed by the trigger.

""")
