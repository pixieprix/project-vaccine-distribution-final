-- 12 explicit tables in excel


-- need to check:
--phone number no. of digits
--when must non-key attributes have non-null constraints e.g. patient name?




CREATE TABLE if NOT EXISTS VaccineType (
    ID VARCHAR(255) NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    doses INT NOT NULL,
    tempMin INT,
    tempMax INT
);

CREATE TABLE if NOT EXISTS Manufacturer (
    ID VARCHAR(255) NOT NULL PRIMARY KEY,
    country CHAR(255) NOT NULL,
    phone VARCHAR(20),
    vaccine VARCHAR(255),
    FOREIGN KEY (vaccine) REFERENCES VaccineType(ID)
);

CREATE TABLE if NOT EXISTS VaccinationStations (
    name VARCHAR(255) NOT NULL PRIMARY KEY,
    address VARCHAR(255),
    phone VARCHAR(13)
);

CREATE TABLE if NOT EXISTS VaccineBatch (
    batchID VARCHAR(255) NOT NULL PRIMARY KEY,
    amount INT NOT NULL,
    type VARCHAR(255),
    manufacturer VARCHAR(255),
    manufDate DATE,
    expiration DATE,
    location VARCHAR(255),
    FOREIGN KEY (type) REFERENCES VaccineType(ID),
    FOREIGN KEY (manufacturer) REFERENCES Manufacturer(ID),
    FOREIGN KEY (location) REFERENCES VaccinationStations(name)
);

CREATE TABLE if NOT EXISTS TransportationLog (
    batchID VARCHAR(255) NOT NULL,
    arrival VARCHAR(255) NOT NULL,
    departure VARCHAR(255) NOT NULL,
    dateArr DATE NOT NULL,
    dateDep DATE NOT NULL,
    PRIMARY KEY (batchID, arrival, departure, dateArr, dateDep),
    FOREIGN KEY (batchID) REFERENCES VaccineBatch(batchID),
    FOREIGN KEY (arrival) REFERENCES VaccinationStations(name),
    FOREIGN KEY (departure) REFERENCES VaccinationStations(name)
);

CREATE TABLE if NOT EXISTS Staffmembers (
    social_security_number VARCHAR(255) NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    DOB DATE,
    phone VARCHAR(13),
    role VARCHAR(10),
    vaccination_status BOOL,
    hospital VARCHAR(255) REFERENCES VaccinationStations(name),
    CHECK (role IN ('nurse', 'doctor'))
);

CREATE TABLE if NOT EXISTS Shifts (
    station VARCHAR(255) REFERENCES VaccinationStations(name),
    weekday INT CHECK (weekday BETWEEN 0 AND 6),
    worker VARCHAR(255) REFERENCES Staffmembers(social_security_number),
    PRIMARY KEY (station, weekday, worker)
);

--renamed attribute date -> vacc_date to not confuse with attribute type
CREATE TABLE if NOT EXISTS Vaccinations (
    vacc_date DATE NOT NULL,
    location VARCHAR(255) NOT NULL REFERENCES VaccinationStations(name),
    batchID VARCHAR(255) REFERENCES VaccineBatch(batchID),
    PRIMARY KEY (vacc_date, location)
);

CREATE TABLE if NOT EXISTS Patients (
    ssNo VARCHAR(255) NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    DOB DATE,
    gender VARCHAR,
    CHECK (gender IN ('M', 'F'))
);

CREATE TABLE if NOT EXISTS VaccinePatients (
    vacc_date DATE NOT NULL,
    location VARCHAR(255) NOT NULL,
    patientSsNo VARCHAR(255) NOT NULL REFERENCES Patients(ssNo),
    PRIMARY KEY (vacc_date, location, patientSsNo),
    CONSTRAINT vacc_date_location FOREIGN KEY (vacc_date, location) REFERENCES Vaccinations(vacc_date, location)
);

CREATE TABLE if NOT EXISTS Symptoms (
    name VARCHAR(255) NOT NULL PRIMARY KEY,
    criticality BOOL
);

CREATE TABLE IF NOT EXISTS Diagnosis (
    id SERIAL PRIMARY KEY,
    patient VARCHAR(255) NOT NULL REFERENCES Patients(ssNo),
    symptom VARCHAR(255) NOT NULL REFERENCES Symptoms(name),
    diagnosis_date DATE
);



