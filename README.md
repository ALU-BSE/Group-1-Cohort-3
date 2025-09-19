-----------------------------------------

Project: MoMo SMS ETL + Dashboard

Team Packet Sniffers

-----------------------------------------

Project Description

This repository implements an enterprise-like full-stack application that ingests MoMo SMS data in XML format, cleans and categorizes transactions, stores them in a relational database (SQLite for development), and exposes the cleaned data to a lightweight dashboard.

----------------------------------------

High Level System Architecture:

https://drive.google.com/file/d/1MzF3M-PMONt0YPIuAqFXE-lWjggoucyt/view?usp=sharing

----------------------------------------

Database Documentation

We designed a database for our web app that will store mobile money information and separate it into categories that allow for easy analysis and display on our web app. The entities we identified are the user, the transactions, the transaction categories, the sms, the system log, the sms backup, and the service center. The attributes for the users include a type to identify the different types of users (regular, agents, etc) to differentiate between transactions better. The transactions entity uses the private key of the user entity in order to identify the sender and the receiver, and this was designed this way to avoid confusion and to properly organize the data. The transaction category will have more details on what type of transaction occurred, which will help with identifying the fees. We included the system log to track transaction processes and find errors or delays quickly and efficiently. After analyzing the XML file, we noticed the first line was of some sort of backup, so we added it as an entity that interacts with the sms and backs it up. Finally, the service center entity provides its private key to the sms entity for easier organization. 
Amounts transferred are in integer format, dates and times are formatted in DATETIME, and the other attributes are formatted in varchar. This allows for flexibility in naming and such. Overall, our design allows for easy viewing and accessing of data. 

----------------------------------------

Members:

Sedem Amuzu (GitHub: @SamuzuKofi)

Joshua Agonzibwa (GitHub: @jagonzibwa)

Larry Sentore (GitHub: @Larry-Sentore)

----------------------------------------
