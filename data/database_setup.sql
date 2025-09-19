CREATE TABLE `Transaction Category` (
  `Category_id` VARCHAR(50),
  `Payment_type` VARCHAR(50),
  `Transfer_type` VARCHAR(50),
  PRIMARY KEY (`Category_id`)
);

CREATE TABLE `System Log` (
  `Log_id` VARCHAR(50),
  `Transaction_id` VARCHAR(50),
  `level` VARCHAR(50),
  `Component` INT,
  `payload` VARCHAR(255),
  `created_at` TIMESTAMP,
  PRIMARY KEY (`Log_id`)
);

CREATE TABLE `Service Centre` (
  `Service_center_id` VARCHAR(50),
  `Phone Number` VARCHAR(50),
  `ISP_Name` VARCHAR(250),
  PRIMARY KEY (`Service_center_id`)
);

CREATE TABLE `User` (
  `User_id` VARCHAR(50),
  `Name` VARCHAR(255),
  `mobile_number` VARCHAR(50),
  `User_type` VARCHAR(50),
  `created_at` TIMESTAMP,
  PRIMARY KEY (`User_id`)
);

CREATE TABLE `Backup` (
  `Backup_id` VARCHAR(50),
  `Backup_set` VARCHAR(50),
  `Backup_date` INT,
  `Type` VARCHAR(50),
  `Count` INT,
  PRIMARY KEY (`Backup_id`)
);

CREATE TABLE `SMS` (
  `SMS_id` VARCHAR(50),
  `Transaction_id` VARCHAR(50),
  `Protocol` INT,
  `Address` VARCHAR(50),
  `Date_sent` TIMESTAMP,
  `Type` INT,
  `Subject` VARCHAR(255),
  `SMS_Body` VARCHAR(500),
  `Read` INT,
  `Status` INT,
  `Sub_ID` VARCHAR(50),
  PRIMARY KEY (`SMS_id`)
);

CREATE TABLE `Transaction` (
  `Transaction_id` VARCHAR(50),
  `Sender_id` VARCHAR(50),
  `Receiver_id` VARCHAR(50),
  `Transaction_category_id` VARCHAR(50),
  `Amount` INT,
  `Currency` VARCHAR(10),
  `Status` VARCHAR(20),
  `recieved_at` TIMESTAMP,
  `balance_after` INT,
  `created_at` TIMESTAMP,
  `Transaction Type` VARCHAR(50),
  PRIMARY KEY (`Transaction_id`),
  FOREIGN KEY (`Transaction_id`)
      REFERENCES `User`(`User_id`),
  FOREIGN KEY (`Transaction_category_id`)
      REFERENCES `Transaction Category`(`Category_id`)
);

