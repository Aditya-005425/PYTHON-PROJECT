-- Create TaxPayers table
CREATE TABLE TaxPayers (
    TaxPayerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Phone VARCHAR(15),
    Address VARCHAR(255),
    TaxIdentificationNumber VARCHAR(20)
);

-- Create TaxRates table
CREATE TABLE TaxRates (
    TaxRateID INT AUTO_INCREMENT PRIMARY KEY,
    IncomeBracket VARCHAR(50),
    RatePercentage DECIMAL(5,2)
);

-- Create TaxReturns table
CREATE TABLE TaxReturns (
    TaxReturnID INT AUTO_INCREMENT PRIMARY KEY,
    TaxPayerID INT,
    TotalIncome DECIMAL(15,2),
    TaxableIncome DECIMAL(15,2),
    TaxAmount DECIMAL(15,2),
    Status VARCHAR(50),
    FOREIGN KEY (TaxPayerID) REFERENCES TaxPayers(TaxPayerID)
);

-- Create Deductions table
CREATE TABLE Deductions (
    DeductionID INT AUTO_INCREMENT PRIMARY KEY,
    TaxPayerID INT,
    DeductionType VARCHAR(100),
    DeductionAmount DECIMAL(15,2),
    FilingYear INT,
    FOREIGN KEY (TaxPayerID) REFERENCES TaxPayers(TaxPayerID)
);

-- Create Penalties table
CREATE TABLE Penalties (
    PenaltyID INT AUTO_INCREMENT PRIMARY KEY,
    TaxPayerID INT,
    Amount DECIMAL(15,2),
    Reason VARCHAR(255),
    Status VARCHAR(50),
    FOREIGN KEY (TaxPayerID) REFERENCES TaxPayers(TaxPayerID)
);

-- Create TaxConsultants table
CREATE TABLE TaxConsultants (
    ConsultantID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Phone VARCHAR(15),
    Expertise VARCHAR(100)
);

-- Create TaxConsultantAssignments table
CREATE TABLE TaxConsultantAssignments (
    AssignmentID INT AUTO_INCREMENT PRIMARY KEY,
    TaxPayerID INT,
    ConsultantID INT,
    FOREIGN KEY (TaxPayerID) REFERENCES TaxPayers(TaxPayerID),
    FOREIGN KEY (ConsultantID) REFERENCES TaxConsultants(ConsultantID)
);




-- Insert data into TaxPayers table
INSERT INTO TaxPayers (Name, Email, Phone, Address, TaxIdentificationNumber) 
VALUES ('Jon Snow', 'jon@gmail.com', '1234567890', '123 Elm Street', 'TAX1234567'),
       ('Peter Parker', 'peter@gmail.com', '9876543210', '456 Oak Avenue', 'TAX7654321'),
       ('Barry Allen', 'barry@gmail.com', '2345678901', '789 Pine Road', 'TAX2345678'),
       ('Diana Prince', 'daina@gmail.com', '3456789012', '321 Maple Drive', 'TAX3456789'),
       ('Clarke Kent', 'clarke@gmail.com', '4567890123', '654 Cedar Lane', 'TAX4567890'),
       ('Wade Wilson', 'wade@gmail.com', '5678901234', '987 Birch Court', 'TAX5678901'),
       ('Bruce Wayne', 'bruce@gmail.com', '5671341234', '987 Gotham', 'TAX9998901'),
       ('Tony Stark', 'tony@gmail.com', '5673000234', '987 New York', 'TAX9888901');

-- Insert data into TaxRates table
INSERT INTO TaxRates (IncomeBracket, RatePercentage) 
VALUES ('0-300000', 0),
       ('300001-700000', 5),
       ('700001-1000000', 10),
       ('1000001-1200000', 15),
       ('1200001 and 1500000', 20),
       ('1500001 and above', 30);

-- Insert data into TaxReturns table
INSERT INTO TaxReturns (TaxPayerID, TotalIncome, TaxableIncome, TaxAmount, Status) 
VALUES (1, 75000, 70000, 7000, 'Filed'),
       (2, 150000, 140000, 21000, 'Pending'),
       (3, 200000, 180000, 27000, 'Filed'),
       (4, 400000, 350000, 70000, 'Pending'),
       (5, 850000, 800000, 240000, 'Filed'),
       (6, 1000000, 950000, 382500, 'Filed'),
       (7, 1200000, 1150000, 405000, 'Filed'),
       (8, 1100000, 1050000, 404000, 'Filed');

-- Insert data into Deductions table
INSERT INTO Deductions (TaxPayerID, DeductionType, DeductionAmount, FilingYear) 
VALUES (1, 'Medical Expenses', 5000, 2024),
       (2, 'Education Loan', 10000, 2024),
       (3, 'Charity Donations', 15000, 2024),
       (4, 'Home Loan Interest', 20000, 2024),
       (5, 'Retirement Savings', 30000, 2024),
       (6, 'Health Insurance', 25000, 2024),
       (7, 'Health Insurance', 22000, 2024),
       (8, 'Health Insurance', 20000, 2024);

-- Insert data into Penalties table
INSERT INTO Penalties (TaxPayerID, Amount, Reason, Status) 
VALUES (1, 200.00, 'Late Filing Fee', 'Unpaid'),
       (2, 500.00, 'Audit Penalty', 'Paid'),
       (3, 300.00, 'Missed Payment Deadline', 'Unpaid'),
       (4, 150.00, 'Underreported Income', 'Paid'),
       (5, 500.00, 'Late Payment Fee', 'Unpaid'),
       (6, 1000.00, 'Non-Compliance with Audit', 'Paid'),
       (7, 500.00, 'Non-Compliance with Audit', 'Paid'),
       (8, 1000.00, 'Late Payment Fee', 'Unpaid');

-- Insert data into TaxConsultants table
INSERT INTO TaxConsultants (Name, Email, Phone, Expertise) 
VALUES ('Alice Brown', 'alice.brown@consultants.com', '1122334455', 'Income Tax'),
       ('Robert Green', 'robert.green@consultants.com', '2233445566', 'Corporate Tax'),
       ('David Miller', 'david.miller@consultants.com', '3344556677', 'Tax Law'),
       ('Olivia Garcia', 'olivia.garcia@consultants.com', '4455667788', 'Corporate Tax');

-- Insert data into TaxConsultantAssignments table
INSERT INTO TaxConsultantAssignments (TaxPayerID, ConsultantID) 
VALUES (1, 1),
       (2, 2),
       (3, 3),
       (4, 4),
       (5, 1),
       (6, 2),
       (7, 3),
       (8, 4);

