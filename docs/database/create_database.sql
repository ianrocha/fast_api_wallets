-- MySQL Workbench Forward Engineering

-- -----------------------------------------------------
-- Schema fast_api_wallet
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `fast_api_wallet` DEFAULT CHARACTER SET utf8mb4;
USE `fast_api_wallet` ;

-- -----------------------------------------------------
-- Table `fast_api_wallet`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fast_api_wallet`.`users` (
  `user_id` INT NOT NULL auto_increment,
  `name` VARCHAR(50) NOT NULL,
  `document` VARCHAR(16) NOT NULL UNIQUE,
  `email` VARCHAR(50) NOT NULL UNIQUE,
  `password` VARCHAR(16) NOT NULL,
  `is_shopkeeper` BOOLEAN,
  `is_active` BOOLEAN,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `fast_api_wallet`.`wallets`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fast_api_wallet`.`wallets` (
  `wallet_id` INT NOT NULL auto_increment,
  `user_id` INT NOT NULL,
  `total` FLOAT NOT NULL,
  INDEX `fk_user_id_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_id_idx`
    FOREIGN KEY (`user_id`)
    REFERENCES `fast_api_wallet`.`users` (`user_id`),
  PRIMARY KEY (`wallet_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fast_api_wallet`.`transaction_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fast_api_wallet`.`transaction_type` (
  `transaction_type_id` INT NOT NULL auto_increment,
  `transaction_type_description` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`transaction_type_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fast_api_wallet`.`financial_transactions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fast_api_wallet`.`financial_transactions` (
  `transaction_id` INT NOT NULL auto_increment,
  `origin_wallet_id` INT,
  `destination_wallet_id` INT,
  `transaction_type_id` INT NOT NULL,
  `movement_value` FLOAT NOT NULL,
  `operation_date` DATETIME,
  INDEX `fk_origin_wallet_id_idx` (`origin_wallet_id` ASC),
  INDEX `fk_destination_wallet_id_idx` (`destination_wallet_id` ASC),
  INDEX `fk_transaction_type_id_idx` (`transaction_type_id` ASC),
  CONSTRAINT `fk_origin_wallet_id_idx`
    FOREIGN KEY (`origin_wallet_id`)
    REFERENCES `fast_api_wallet`.`wallets` (`wallet_id`),
  CONSTRAINT `fk_destination_wallet_id_idx`
    FOREIGN KEY (`destination_wallet_id`)
    REFERENCES `fast_api_wallet`.`wallets` (`wallet_id`),
  CONSTRAINT `fk_transaction_type_id_idx`
    FOREIGN KEY (`transaction_type_id`)
    REFERENCES `fast_api_wallet`.`transaction_type` (`transaction_type_id`),
  PRIMARY KEY (`transaction_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- INSERT INTO Table `fast_api_wallet`.`transaction_type`
-- -----------------------------------------------------
INSERT INTO fast_api_wallet.transaction_type (transaction_type_id, transaction_type_description)
VALUES (1, "withdraw");
INSERT INTO fast_api_wallet.transaction_type (transaction_type_id, transaction_type_description)
VALUES (2, "transfer");
INSERT INTO fast_api_wallet.transaction_type (transaction_type_id, transaction_type_description)
VALUES (3, "deposit");

-- -----------------------------------------------------
-- INSERT INTO Table `fast_api_wallet`.`users`
-- -----------------------------------------------------
INSERT INTO fast_api_wallet.users (user_id, name, document, email, password, is_shopkeeper, is_active)
VALUES (4, "Ian", "1234", "test@test.com", "4321", 0, 1);
INSERT INTO fast_api_wallet.users (user_id, name, document, email, password, is_shopkeeper, is_active)
VALUES (6, "Zeca", "43215", "test2@test.com", "56742dfa" , 1, 1);
INSERT INTO fast_api_wallet.users (user_id, name, document, email, password, is_shopkeeper, is_active)
VALUES (10, "Joaquim", "432165", "test23@test.com", "56742dfa" , 1, 1);
INSERT INTO fast_api_wallet.users (user_id, name, document, email, password, is_shopkeeper, is_active)
VALUES (15, "Joaozinho", "4553768", "test3@test.com", "asdvgbtjt" , 1, 1);

-- -----------------------------------------------------
-- INSERT INTO Table `fast_api_wallet`.`wallets`
-- -----------------------------------------------------
INSERT INTO fast_api_wallet.wallets (wallet_id, user_id, total)
VALUES (5, 10, 60000);
INSERT INTO fast_api_wallet.wallets (wallet_id, user_id, total)
VALUES (4, 4, 1395);
INSERT INTO fast_api_wallet.wallets (wallet_id, user_id, total)
VALUES (3, 15, 2095);
INSERT INTO fast_api_wallet.wallets (wallet_id, user_id, total)
VALUES (6, 6, 750);

-- -----------------------------------------------------
-- INSERT INTO Table `fast_api_wallet`.`financial_transactions`
-- -----------------------------------------------------
INSERT INTO fast_api_wallet.financial_transactions (transaction_id, origin_wallet_id, destination_wallet_id, transaction_type_id, movement_value, operation_date)
VALUES (1, 4, 3, 2, 15, "2021-08-28 12:00:02");
INSERT INTO fast_api_wallet.financial_transactions (transaction_id, origin_wallet_id, destination_wallet_id, transaction_type_id, movement_value, operation_date)
VALUES (2, 4, 3, 2, 15, "2021-08-28 12:00:02");
INSERT INTO fast_api_wallet.financial_transactions (transaction_id, origin_wallet_id, destination_wallet_id, transaction_type_id, movement_value, operation_date)
VALUES (3, 4, 3, 2, 15, "2021-08-28 12:00:02");
INSERT INTO fast_api_wallet.financial_transactions (transaction_id, origin_wallet_id, destination_wallet_id, transaction_type_id, movement_value, operation_date)
VALUES (4, 4, 3, 2, 150, "2021-08-28 16:05:36");
INSERT INTO fast_api_wallet.financial_transactions (transaction_id, origin_wallet_id, destination_wallet_id, transaction_type_id, movement_value, operation_date)
VALUES (5, 4, 3, 2, 150, "2021-08-28 16:05:36");
INSERT INTO fast_api_wallet.financial_transactions (transaction_id, origin_wallet_id, destination_wallet_id, transaction_type_id, movement_value, operation_date)
VALUES (6, 4, 3, 2, 150, "2021-08-28 16:05:36");
INSERT INTO fast_api_wallet.financial_transactions (transaction_id, origin_wallet_id, destination_wallet_id, transaction_type_id, movement_value, operation_date)
VALUES (7, 4, 3, 2, 5, "2021-08-28 16:05:36");
INSERT INTO fast_api_wallet.financial_transactions (transaction_id, origin_wallet_id, destination_wallet_id, transaction_type_id, movement_value, operation_date)
VALUES (8, 4, 3, 2, 5, "2021-08-28 16:05:36");
INSERT INTO fast_api_wallet.financial_transactions (transaction_id, origin_wallet_id, destination_wallet_id, transaction_type_id, movement_value, operation_date)
VALUES (9, 4, 3, 2, 5, "2021-08-28 16:50:39");
