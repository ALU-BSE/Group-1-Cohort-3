-- =========================
-- DDL: Table Definitions
-- =========================

CREATE TABLE `Transaction Category` (
  `Category_id` VARCHAR(50) PRIMARY KEY,
  `Payment_type` VARCHAR(50),
  `Transfer_type` VARCHAR(50)
);

CREATE TABLE `System Log` (
  `Log_id` VARCHAR(50) PRIMARY KEY,
  `Transaction_id` VARCHAR(50),
  `level` VARCHAR(50),
  `Component` INT,
  `payload` VARCHAR(255),
  `created_at` TIMESTAMP
);

CREATE TABLE `Service Centre` (
  `Service_center_id` VARCHAR(50) PRIMARY KEY,
  `Phone Number` VARCHAR(50),
  `ISP_Name` VARCHAR(250)
);

CREATE TABLE `User` (
  `User_id` VARCHAR(50) PRIMARY KEY,
  `Name` VARCHAR(255),
  `mobile_number` VARCHAR(50),
  `User_type` VARCHAR(50),
  `created_at` TIMESTAMP
);

CREATE TABLE `Backup` (
  `Backup_id` VARCHAR(50) PRIMARY KEY,
  `Backup_set` VARCHAR(50),
  `Backup_date` INT,
  `Type` VARCHAR(50),
  `Count` INT
);

CREATE TABLE `SMS` (
  `SMS_id` VARCHAR(50) PRIMARY KEY,
  `Transaction_id` VARCHAR(50),
  `Protocol` INT,
  `Address` VARCHAR(50),
  `Date_sent` TIMESTAMP,
  `Type` INT,
  `Subject` VARCHAR(255),
  `SMS_Body` VARCHAR(500),
  `Read` INT,
  `Status` INT,
  `Sub_ID` VARCHAR(50)
);

CREATE TABLE `Transaction` (
  `Transaction_id` VARCHAR(50) PRIMARY KEY,
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
  FOREIGN KEY (`Sender_id`) REFERENCES `User`(`User_id`),
  FOREIGN KEY (`Receiver_id`) REFERENCES `User`(`User_id`),
  FOREIGN KEY (`Transaction_category_id`) REFERENCES `Transaction Category`(`Category_id`)
);

CREATE INDEX idx_transaction_sender ON `Transaction` (`Sender_id`);
CREATE INDEX idx_transaction_receiver ON `Transaction` (`Receiver_id`);
CREATE INDEX idx_transaction_category ON `Transaction` (`Transaction_category_id`);
CREATE INDEX idx_sms_transaction ON `SMS` (`Transaction_id`);
CREATE INDEX idx_systemlog_transaction ON `System Log` (`Transaction_id`);
CREATE INDEX idx_user_mobile ON `User` (`mobile_number`);


-- Transaction Category
INSERT INTO `Transaction Category` VALUES
  ('cat1', 'Payment', 'Bank Transfer'),
  ('cat2', 'Withdrawal', 'ATM'),
  ('cat3', 'Deposit', 'Mobile Money'),
  ('cat4', 'Payment', 'Card'),
  ('cat5', 'Transfer', 'Online');

-- User
INSERT INTO `User` VALUES
  ('u1', 'Alice Smith', '0791000001', 'customer', NOW()),
  ('u2', 'Bob Jones', '0791000002', 'customer', NOW()),
  ('u3', 'Carol White', '0791000003', 'admin', NOW()),
  ('u4', 'David Black', '0791000004', 'customer', NOW()),
  ('u5', 'Eve Green', '0791000005', 'customer', NOW());

-- Service Centre
INSERT INTO `Service Centre` VALUES
  ('sc1', '0792000001', 'MTN'),
  ('sc2', '0792000002', 'MTN'),
  ('sc3', '0792000003', 'MTN'),
  ('sc4', '0792000004', 'MTN'),
  ('sc5', '0792000005', 'MTN');

-- Transaction
INSERT INTO `Transaction` VALUES
  ('t1', 'u1', 'u2', 'cat1', 100, 'RWF', 'completed', NOW(), 900, NOW(), 'Payment'),
  ('t2', 'u2', 'u3', 'cat2', 200, 'RWF', 'pending', NOW(), 800, NOW(), 'Withdrawal'),
  ('t3', 'u3', 'u4', 'cat3', 300, 'RWF', 'completed', NOW(), 700, NOW(), 'Deposit'),
  ('t4', 'u4', 'u5', 'cat4', 400, 'RWF', 'failed', NOW(), 600, NOW(), 'Payment'),
  ('t5', 'u5', 'u1', 'cat5', 500, 'RWF', 'completed', NOW(), 500, NOW(), 'Transfer');

-- SMS
INSERT INTO `SMS` VALUES
  ('sms1', 't1', 1, '0791000001', NOW(), 1, 'Subject1', 'Payment received', 1, 0, 'sub1'),
  ('sms2', 't2', 1, '0791000002', NOW(), 1, 'Subject2', 'Withdrawal pending', 0, 1, 'sub2'),
  ('sms3', 't3', 1, '0791000003', NOW(), 1, 'Subject3', 'Deposit completed', 1, 0, 'sub3'),
  ('sms4', 't4', 1, '0791000004', NOW(), 1, 'Subject4', 'Payment failed', 0, 1, 'sub4'),
  ('sms5', 't5', 1, '0791000005', NOW(), 1, 'Subject5', 'Transfer completed', 1, 0, 'sub5');

-- System Log
INSERT INTO `System Log` VALUES
  ('log1', 't1', 'INFO', 1, 'Transaction processed', NOW()),
  ('log2', 't2', 'WARN', 2, 'Transaction pending', NOW()),
  ('log3', 't3', 'INFO', 1, 'Deposit successful', NOW()),
  ('log4', 't4', 'ERROR', 3, 'Payment failed', NOW()),
  ('log5', 't5', 'INFO', 1, 'Transfer completed', NOW());

-- Backup
INSERT INTO `Backup` VALUES
  ('b1', 'set1', 20230901, 'Full', 5),
  ('b2', 'set2', 20230902, 'Incremental', 3),
  ('b3', 'set3', 20230903, 'Full', 6),
  ('b4', 'set4', 20230904, 'Differential', 2),
  ('b5', 'set5', 20230905, 'Full', 7);