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

## Database Documentation

We designed a database for our web app that will store mobile money information and separate it into categories that allow for easy analysis and display on our web app. The entities we identified are the user, the transactions, the transaction categories, the sms, the system log, the sms backup, and the service center. The attributes for the users include a type to identify the different types of users (regular, agents, etc) to differentiate between transactions better. The transactions entity uses the private key of the user entity in order to identify the sender and the receiver, and this was designed this way to avoid confusion and to properly organize the data. The transaction category will have more details on what type of transaction occurred, which will help with identifying the fees. We included the system log to track transaction processes and find errors or delays quickly and efficiently. After analyzing the XML file, we noticed the first line was of some sort of backup, so we added it as an entity that interacts with the sms and backs it up. Finally, the service center entity provides its private key to the sms entity for easier organization. 
Amounts transferred are in integer format, dates and times are formatted in DATETIME, and the other attributes are formatted in varchar. This allows for flexibility in naming and such. Overall, our design allows for easy viewing and accessing of data. 

---

### Database Schema & Sample Data

```sql
-- Drop triggers
DROP TRIGGER IF EXISTS generate_category_id;
DROP TRIGGER IF EXISTS generate_log_id;
DROP TRIGGER IF EXISTS generate_service_center_id;
DROP TRIGGER IF EXISTS generate_user_id;
DROP TRIGGER IF EXISTS generate_Backup_id;
DROP TRIGGER IF EXISTS generate_sms_id;
DROP TRIGGER IF EXISTS generate_transaction_id;

-- Drop tables (drop child tables before parent tables to avoid FK errors)
DROP TABLE IF EXISTS `SMS`;
DROP TABLE IF EXISTS `Transaction`;
DROP TABLE IF EXISTS `Backup`;
DROP TABLE IF EXISTS `User`;
DROP TABLE IF EXISTS `Service Centre`;
DROP TABLE IF EXISTS `System Log`;
DROP TABLE IF EXISTS `Transaction Category`;

-- Drop sequence tables last
DROP TABLE IF EXISTS `SMS_sequence`;
DROP TABLE IF EXISTS `Transaction_sequence`;
DROP TABLE IF EXISTS `Backup_sequence`;
DROP TABLE IF EXISTS `User_sequence`;
DROP TABLE IF EXISTS `Service_sequence`;
DROP TABLE IF EXISTS `Log_sequence`;
DROP TABLE IF EXISTS `Category_sequence`;

-- Transaction Category
CREATE TABLE `Category_sequence`(
  `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT
);

CREATE TABLE `Transaction Category` (
  `Category_id` VARCHAR(50) PRIMARY KEY NOT NULL,
  `Payment_type` VARCHAR(50),
  `Transfer_type` VARCHAR(50)
);

DELIMITER //
CREATE TRIGGER generate_category_id
BEFORE INSERT ON `Transaction Category`
FOR EACH ROW
BEGIN
  INSERT INTO `Category_sequence` VALUES (NULL);
  SET NEW.Category_id = CONCAT('TCAT', LPAD(LAST_INSERT_ID(), 4, '0'));
END//
DELIMITER ;

-- System Log
CREATE TABLE `Log_sequence`(
  `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT
);

CREATE TABLE `System Log` (
  `Log_id` VARCHAR(50) PRIMARY KEY NOT NULL,
  `Transaction_id` VARCHAR(50),
  `level` VARCHAR(50),
  `Component` INT,
  `payload` VARCHAR(255),
  `created_at` TIMESTAMP
);

DELIMITER //
CREATE TRIGGER generate_log_id
BEFORE INSERT ON `System Log`
FOR EACH ROW
BEGIN
  INSERT INTO `Log_sequence` VALUES (NULL);
  SET NEW.Log_id = CONCAT('SLOG', LPAD(LAST_INSERT_ID(), 4, '0'));
END//
DELIMITER ;

-- Service Centre
CREATE TABLE `Service_sequence`(
  `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT
);

CREATE TABLE `Service Centre` (
  `Service_center_id` VARCHAR(50) PRIMARY KEY NOT NULL,
  `Mobile_number` VARCHAR(50),
  `ISP_Name` VARCHAR(250)
);

DELIMITER //
CREATE TRIGGER generate_service_center_id
BEFORE INSERT ON `Service Centre`
FOR EACH ROW
BEGIN
  INSERT INTO `Service_sequence` VALUES (NULL);
  SET NEW.Service_center_id = CONCAT('SC', LPAD(LAST_INSERT_ID(), 4, '0'));
END//
DELIMITER ;

-- User
CREATE TABLE `User_sequence`(
  `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT
);

CREATE TABLE `User` (
  `User_id` VARCHAR(50) PRIMARY KEY NOT NULL,
  `First_name` VARCHAR(255),
  `Last_name` VARCHAR(255),
  `Mobile_number` VARCHAR(50),
  `User_type` VARCHAR(50),
  `Created_at` TIMESTAMP
);

DELIMITER //
CREATE TRIGGER generate_user_id
BEFORE INSERT ON `User`
FOR EACH ROW
BEGIN
  INSERT INTO `User_sequence` VALUES (NULL);
  SET NEW.User_id = CONCAT('US', LPAD(LAST_INSERT_ID(), 4, '0'));
END//
DELIMITER ;

-- Backup
CREATE TABLE `Backup_sequence`(
  `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT
);

CREATE TABLE `Backup` (
  `Backup_id` VARCHAR(50) PRIMARY KEY NOT NULL,
  `Backup_set` VARCHAR(255),
  `Backup_date` TIMESTAMP,
  `Type` VARCHAR(50),
  `Count` INT
);

DELIMITER //
CREATE TRIGGER generate_Backup_id
BEFORE INSERT ON `Backup`
FOR EACH ROW
BEGIN
  INSERT INTO `Backup_sequence` VALUES (NULL);
  SET NEW.Backup_id = CONCAT('BCK', LPAD(LAST_INSERT_ID(), 4, '0'));
END//
DELIMITER ;

-- SMS
CREATE TABLE `SMS_sequence`(
  `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT
);

CREATE TABLE `SMS` (
  `SMS_id` VARCHAR(50) PRIMARY KEY NOT NULL,
  `Transaction_id` VARCHAR(50),
  `Protocol` INT,
  `Address` VARCHAR(50),
  `Date_sent` TIMESTAMP,
  `Type` INT,
  `Subject` VARCHAR(255),
  `SMS_Body` VARCHAR(500),
  `Read` INT,
  `Status` INT,
  `Sub_id` VARCHAR(50)
);

DELIMITER //
CREATE TRIGGER generate_sms_id
BEFORE INSERT ON `SMS`
FOR EACH ROW
BEGIN
  INSERT INTO `SMS_sequence` VALUES (NULL);
  SET NEW.SMS_id = CONCAT('SMS', LPAD(LAST_INSERT_ID(), 4, '0'));
END//
DELIMITER ;

-- Transaction
CREATE TABLE `Transaction_sequence`(
  `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT
);

CREATE TABLE `Transaction` (
  `Transaction_id` VARCHAR(50) PRIMARY KEY NOT NULL,
  `Sender_id` VARCHAR(50),
  `Receiver_id` VARCHAR(50),
  `Transaction_category_id` VARCHAR(50),
  `Amount` FLOAT CHECK (Amount >= 0),
  `Currency` VARCHAR(10),
  `Status` VARCHAR(20),
  `Recieved_at` TIMESTAMP,
  `Balance_after` FLOAT CHECK (balance_after >= 0),
  `created_at` TIMESTAMP,
  `Transaction Type` VARCHAR(50),
  FOREIGN KEY (`Sender_id`) REFERENCES `User`(`User_id`),
  FOREIGN KEY (`Receiver_id`) REFERENCES `User`(`User_id`),
  FOREIGN KEY (`Transaction_category_id`) REFERENCES `Transaction Category`(`Category_id`)
);

DELIMITER //
CREATE TRIGGER generate_transaction_id
BEFORE INSERT ON `Transaction`
FOR EACH ROW
BEGIN
  INSERT INTO `Transaction_sequence` VALUES (NULL);
  SET NEW.Transaction_id = CONCAT('TRNS', LPAD(LAST_INSERT_ID(), 4, '0'));
END//
DELIMITER ;

CREATE INDEX idx_transaction_sender ON `Transaction` (`Sender_id`);
CREATE INDEX idx_transaction_receiver ON `Transaction` (`Receiver_id`);
CREATE INDEX idx_transaction_category ON `Transaction` (`Transaction_category_id`);
CREATE INDEX idx_sms_transaction ON `SMS` (`Transaction_id`);
CREATE INDEX idx_systemlog_transaction ON `System Log` (`Transaction_id`);
CREATE INDEX idx_user_mobile ON `User` (`mobile_number`);

-- Transaction Category
INSERT INTO `Transaction Category` (`Payment_type`, `Transfer_type`) VALUES
  ('Payment', 'Bank Transfer'),
  ('Withdrawal', 'ATM'),
  ('Deposit', 'Mobile Money'),
  ('Payment', 'Card'),
  ('Transfer', 'Online');

-- User
INSERT INTO `User` (`First_name`, `Last_name`, `Mobile_number`, `User_type`, `Created_at`) VALUES
  ('Alice', 'Smith', '0791000001', 'customer', NOW()),
  ('Bob', 'Jones', '0791000002', 'customer', NOW()),
  ('Carol', 'White', '0791000003', 'admin', NOW()),
  ('David', 'Black', '0791000004', 'customer', NOW()),
  ('Eve', 'Green', '0791000005', 'customer', NOW());

-- Service Centre
INSERT INTO `Service Centre` (`Mobile_number`, `ISP_Name`) VALUES
  ('0792000001', 'MTN'),
  ('0792000002', 'MTN'),
  ('0792000003', 'MTN'),
  ('0792000004', 'MTN'),
  ('0792000005', 'MTN');

-- Transaction
INSERT INTO `Transaction` (`Sender_id`, `Receiver_id`, `Transaction_category_id`, `Amount`, `Currency`, `Status`, `Recieved_at`, `Balance_after`, `created_at`, `Transaction Type`) VALUES
  ('US0001', 'US0002', 'TCAT0001', 100, 'RWF', 'completed', NOW(), 900, NOW(), 'Payment'),
  ('US0002', 'US0003', 'TCAT0002', 200, 'RWF', 'pending', NOW(), 800, NOW(), 'Withdrawal'),
  ('US0003', 'US0004', 'TCAT0003', 300, 'RWF', 'completed', NOW(), 700, NOW(), 'Deposit'),
  ('US0004', 'US0005', 'TCAT0004', 400, 'RWF', 'failed', NOW(), 600, NOW(), 'Payment'),
  ('US0005', 'US0001', 'TCAT0005', 500, 'RWF', 'completed', NOW(), 500, NOW(), 'Transfer');

-- SMS
INSERT INTO `SMS` (`Transaction_id`, `Protocol`, `Address`, `Date_sent`, `Type`, `Subject`, `SMS_Body`, `Read`, `Status`, `Sub_id`) VALUES
  ('TRNS0001', 1, '0791000001', NOW(), 1, 'Subject1', 'Payment received', 1, 0, 'sub1'),
  ('TRNS0002', 1, '0791000002', NOW(), 1, 'Subject2', 'Withdrawal pending', 0, 1, 'sub2'),
  ('TRNS0003', 1, '0791000003', NOW(), 1, 'Subject3', 'Deposit completed', 1, 0, 'sub3'),
  ('TRNS0004', 1, '0791000004', NOW(), 1, 'Subject4', 'Payment failed', 0, 1, 'sub4'),
  ('TRNS0005', 1, '0791000005', NOW(), 1, 'Subject5', 'Transfer completed', 1, 0, 'sub5');

-- System Log
INSERT INTO `System Log` (`Transaction_id`, `level`, `Component`, `payload`, `created_at`) VALUES
  ('TRNS0001', 'INFO', 1, 'Transaction processed', NOW()),
  ('TRNS0002', 'WARN', 2, 'Transaction pending', NOW()),
  ('TRNS0003', 'INFO', 1, 'Deposit successful', NOW()),
  ('TRNS0004', 'ERROR', 3, 'Payment failed', NOW()),
  ('TRNS0005', 'INFO', 1, 'Transfer completed', NOW());

-- Backup
INSERT INTO `Backup` (`Backup_set`, `Backup_date`, `Type`, `Count`) VALUES
  ('set1', NOW(), 'Full', 5),
  ('set2', NOW(), 'Incremental', 3),
  ('set3', NOW(), 'Full', 6),
  ('set4', NOW(), 'Differential', 2),
  ('set5', NOW(), 'Full', 7);
```

---

## CRUD Operations

Below are examples of basic CRUD (Create, Read, Update, Delete) operations performed on the database.  
Each operation is illustrated with a screenshot from the `/CRUD operations img/` folder.

#### **Create**
The following screenshot shows a successful insert operation into the `User` table.  
![Create Operation](CRUD%20operations%20img/Create.png)

#### **Read**
The following screenshot shows a successful select operation from the `User` table.  
![Read Operation](CRUD%20operations%20img/Read.png)

#### **Update**
The following screenshot shows a successful update operation on the `User` table.  
![Update Operation](CRUD%20operations%20img/Update.png)

#### **Delete**
The following screenshot shows a successful delete operation from the `User` table.  
![Delete Operation](CRUD%20operations%20img/Delete.png)

---

## Members

Sedem Amuzu (GitHub: [@SamuzuKofi](https://github.com/SamuzuKofi))  
Joshua Agonzibwa (GitHub: [@jagonzibwa](https://github.com/jagonzibwa))  
Larry Sentore (GitHub: [@Larry-Sentore](https://github.com/Larry-Sentore))

----------------------------------------
