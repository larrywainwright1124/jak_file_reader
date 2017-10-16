-- database: walgreens

-- CREATE DATABASE `walgreens` /*!40100 DEFAULT CHARACTER SET utf8 */;
/*
CREATE TABLE `walgreens`.`ac_account` (
  `xid` INT NOT NULL AUTO_INCREMENT,
  `bal_id` INT NOT NULL DEFAULT 0,
  `client_id` INT NOT NULL DEFAULT 0,
  `status` VARCHAR(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`xid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE `walgreens`.`ac_balance` (
  `bal_id` INT NOT NULL AUTO_INCREMENT,
  `open_to_buy` DECIMAL(10,2) NOT NULL DEFAULT 0,
  `cred_lim` DECIMAL(10,2) NOT NULL DEFAULT 0,
  PRIMARY KEY (`bal_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


CREATE TABLE `walgreens`.`ac_card` (
  `cad` INT NOT NULL AUTO_INCREMENT,
  `xid` INT NOT NULL DEFAULT 0,
  `card_number` VARCHAR(20) NOT NULL,
  `expiry_date` DATETIME NULL,
  `card_status` VARCHAR(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`cad`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE `walgreens`.`ac_client` (
  `client_id` INT NOT NULL AUTO_INCREMENT,
  `fname` VARCHAR(50) NULL,
  `lname` VARCHAR(50) NULL,
  `addr1` VARCHAR(50) NULL,
  `addr2` VARCHAR(50) NULL,
  `city` VARCHAR(25) NULL,
  `state` VARCHAR(10) NULL,
  `zip` VARCHAR(5) NULL,
  PRIMARY KEY (`client_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;
*/
