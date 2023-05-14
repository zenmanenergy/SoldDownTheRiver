CREATE TABLE `businesses` (
  `BusinessId` char(39) NOT NULL,
  `BusinessName` varchar(45) DEFAULT NULL,
  `LocationId` char(39) DEFAULT NULL,
  PRIMARY KEY (`BusinessId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `businesshumans` (
  `BusinessId` char(39) NOT NULL,
  `HumanId` char(39) NOT NULL,
  `RoleId` char(39) DEFAULT NULL,
  PRIMARY KEY (`BusinessId`,`HumanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `families` (
  `HumanId` char(39) NOT NULL,
  `FamilyHumanId` char(39) NOT NULL,
  `Relationship` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`HumanId`,`FamilyHumanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `history` (
  `HistoryId` char(39) NOT NULL,
  `TableName` varchar(45) DEFAULT NULL,
  `KeyName` varchar(45) DEFAULT NULL,
  `KeyValue` varchar(156) DEFAULT NULL,
  `UserId` char(39) DEFAULT NULL,
  `Data` varchar(2000) DEFAULT NULL,
  `DateAdded` datetime DEFAULT NULL,
  PRIMARY KEY (`HistoryId`),
  KEY `tableKeyValue` (`TableName`,`KeyName`,`KeyValue`,`UserId`),
  KEY `tableKey` (`TableName`,`KeyName`,`UserId`) /*!80000 INVISIBLE */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `humanroles` (
  `HumanId` char(39) NOT NULL,
  `RoleId` varchar(45) NOT NULL,
  PRIMARY KEY (`HumanId`,`RoleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `humans` (
  `HumanId` char(39) NOT NULL,
  `FirstName` varchar(45) DEFAULT NULL,
  `MiddleName` varchar(45) DEFAULT NULL,
  `LastName` varchar(45) DEFAULT NULL,
  `StartYear` varchar(10) DEFAULT NULL,
  `EndYear` varchar(10) DEFAULT NULL,
  `Notes` text,
  `BirthDate` datetime DEFAULT NULL,
  `BirthPlace` varchar(45) DEFAULT NULL,
  `RaceId` char(39) DEFAULT NULL,
  `PhysicalDescription` varchar(150) DEFAULT NULL,
  `gender` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`HumanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `humansaka` (
  `AKAHumanId` char(39) NOT NULL,
  `HumanId` char(39) NOT NULL,
  `AKAFirstName` varchar(45) DEFAULT NULL,
  `AKAMiddleName` varchar(45) DEFAULT NULL,
  `AKALastName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`AKAHumanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `locations` (
  `LocationId` char(39) NOT NULL,
  `Address` varchar(45) DEFAULT NULL,
  `City` varchar(45) DEFAULT NULL,
  `County` varchar(45) DEFAULT NULL,
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

CREATE TABLE `roles` (
  `RoleId` char(39) NOT NULL,
  `Role` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`RoleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `ships` (
  `ShipId` char(39) NOT NULL,
  `BuildDate` datetime DEFAULT NULL,
  `Notes` varchar(255) DEFAULT NULL,
  `ShipType` varchar(45) DEFAULT NULL,
  `Size` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ShipId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `transactionhumans` (
  `TransactionId` char(39) NOT NULL,
  `HumanId` char(39) NOT NULL,
  `Notes` varchar(45) DEFAULT NULL,
  `Price` float DEFAULT NULL,
  PRIMARY KEY (`TransactionId`,`HumanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `transactions` (
  `TransactionId` char(39) NOT NULL,
  `TransactionDate` datetime DEFAULT NULL,
  `FromBusinessId` char(39) DEFAULT NULL,
  `ToBusinessId` char(39) DEFAULT NULL,
  `TransactionType` varchar(45) DEFAULT NULL,
  `Notes` varchar(255) DEFAULT NULL,
  `Act` varchar(10) DEFAULT NULL,
  `Page` varchar(10) DEFAULT NULL,
  `NotaryBusinessId` char(39) DEFAULT NULL,
  `Volume` varchar(10) DEFAULT NULL,
  `URL` varchar(255) DEFAULT NULL,
  `TranscriberId` char(39) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `NeedsReview` int DEFAULT NULL,
  PRIMARY KEY (`TransactionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `users` (
  `UserId` char(39) NOT NULL,
  `FirstName` varchar(45) DEFAULT NULL,
  `LastName` varchar(45) DEFAULT NULL,
  `Email` varchar(45) DEFAULT NULL,
  `Password` varchar(45) DEFAULT NULL,
  `School` varchar(45) DEFAULT NULL,
  `SemesterYear` varchar(45) DEFAULT NULL,
  `Phone` varchar(45) DEFAULT NULL,
  `UserType` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `usersessions` (
  `SessionId` char(39) DEFAULT NULL,
  `UserId` char(39) NOT NULL,
  `DateAdded` datetime DEFAULT NULL,
  PRIMARY KEY (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `voyagecargo` (
  `CargoId` char(39) NOT NULL,
  `VoyageId` char(39) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `Quantity` float DEFAULT NULL,
  `Value` float DEFAULT NULL,
  `Notes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`CargoId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `voyagehuman` (
  `VoyageId` char(39) NOT NULL,
  `HumanId` char(39) DEFAULT NULL,
  `RoleId` char(39) DEFAULT NULL,
  `Notes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`VoyageId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `voyages` (
  `VoyageId` char(39) NOT NULL,
  `ShipId` char(39) DEFAULT NULL,
  `StartLocationId` char(39) DEFAULT NULL,
  `EndLocationId` char(39) DEFAULT NULL,
  `StartDate` datetime DEFAULT NULL,
  `EndDate` datetime DEFAULT NULL,
  `Notes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`VoyageId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



CREATE USER 'developer'@'localhost' IDENTIFIED BY 'developer';
GRANT ALL PRIVILEGES ON *.* TO 'developer'@'localhost' WITH GRANT OPTION;
