CREATE DATABASE `solddowntheriver` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

CREATE TABLE `businesses` (
  `BusinessId` char(39) NOT NULL,
  `BusinessName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`BusinessId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `humanaka` (
  `HumanAKAId` char(39) NOT NULL,
  `HumanId` char(39) NOT NULL,
  `FirstName` varchar(45) DEFAULT NULL,
  `MiddleName` varchar(45) DEFAULT NULL,
  `LastName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`HumanAKAId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `humans` (
  `HumanId` char(39) NOT NULL,
  `FirstName` varchar(45) DEFAULT NULL,
  `MiddleName` varchar(45) DEFAULT NULL,
  `LastName` varchar(45) DEFAULT NULL,
  `StartYear` int DEFAULT NULL,
  `EndYear` int DEFAULT NULL,
  `Notes` text,
  PRIMARY KEY (`HumanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `locations` (
  `LocationId` char(39) NOT NULL,
  `City` varchar(45) DEFAULT NULL,
  `State` varchar(45) DEFAULT NULL,
  `Country` varchar(45) DEFAULT NULL,
  `Latitude` float DEFAULT NULL,
  `Longitude` float DEFAULT NULL,
  PRIMARY KEY (`LocationId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `notary` (
  `HumanId` char(39) NOT NULL,
  `Language` varchar(45) DEFAULT NULL,
  `StartYear` int DEFAULT NULL,
  `EndYear` int DEFAULT NULL,
  PRIMARY KEY (`HumanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `partners` (
  `HumanId` char(39) NOT NULL,
  `PartnerHumanId` char(39) DEFAULT NULL,
  PRIMARY KEY (`HumanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `role` (
  `HumanId` char(39) NOT NULL,
  `role` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`HumanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `transactions` (
  `TransactionId` char(39) NOT NULL,
  `TransactionDate` datetime DEFAULT NULL,
  `FromHumanId` char(39) DEFAULT NULL,
  `ToHumanId` char(39) DEFAULT NULL,
  `TransactionType` varchar(45) DEFAULT NULL,
  `Notes` varchar(255) DEFAULT NULL,
  `Act` int DEFAULT NULL,
  `Page` int DEFAULT NULL,
  `NotaryHumanId` char(39) DEFAULT NULL,
  `Volume` int DEFAULT NULL,
  `URL` varchar(255) DEFAULT NULL,
  `TranscriberId` char(39) DEFAULT NULL,
  PRIMARY KEY (`TransactionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `transcribers` (
  `TranscriberId` char(39) NOT NULL,
  `FirstName` varchar(45) DEFAULT NULL,
  `LastName` varchar(45) DEFAULT NULL,
  `School` varchar(45) DEFAULT NULL,
  `SemesterYear` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`TranscriberId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `users` (
  `UserId` char(39) NOT NULL,
  `FirstName` varchar(45) DEFAULT NULL,
  `LastName` varchar(45) DEFAULT NULL,
  `Email` varchar(45) DEFAULT NULL,
  `Password` varchar(45) DEFAULT NULL,
  `School` varchar(45) DEFAULT NULL,
  `SemesterYear` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `usersessions` (
  `SessionId` char(39) NOT NULL,
  `UserId` char(39) DEFAULT NULL,
  `DateAdded` datetime DEFAULT NULL,
  PRIMARY KEY (`SessionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
