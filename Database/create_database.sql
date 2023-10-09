CREATE TABLE `businesses` (
  `BusinessId` char(39) NOT NULL,
  `BusinessName` varchar(255) DEFAULT NULL,
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

CREATE TABLE `humanlocations` (
  `HumanId` char(39) COLLATE utf8mb4_general_ci NOT NULL,
  `LocationId` char(39) COLLATE utf8mb4_general_ci NOT NULL,
  `DateCirca` date NOT NULL,
  PRIMARY KEY (`HumanId`,`LocationId`,`DateCirca`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `humanowners` (
  `HumanId` char(39) NOT NULL,
  `OwnerBusinessId` char(39) NOT NULL,
  `OwnDate` datetime DEFAULT NULL,
  `TransactionId` char(39) DEFAULT NULL,
  PRIMARY KEY (`HumanId`,`OwnerBusinessId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `humanroles` (
  `HumanId` varchar(39) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `RoleId` char(39) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`HumanId`,`RoleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `humans` (
  `HumanId` char(39) NOT NULL,
  `FirstName` varchar(155) DEFAULT NULL,
  `MiddleName` varchar(45) DEFAULT NULL,
  `LastName` varchar(155) DEFAULT NULL,
  `Notes` text,
  `BirthDate` datetime DEFAULT NULL,
  `BirthDateAccuracy` varchar(45) DEFAULT NULL,
  `BirthPlace` varchar(45) DEFAULT NULL,
  `RaceId` char(39) DEFAULT NULL,
  `PhysicalDescription` varchar(150) DEFAULT NULL,
  `Gender` varchar(45) DEFAULT NULL,
  `HeightInInches` float DEFAULT NULL,
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
  `Address` varchar(255) DEFAULT NULL,
  `City` varchar(255) DEFAULT NULL,
  `County` varchar(255) DEFAULT NULL,
  `State` varchar(255) DEFAULT NULL,
  `Country` varchar(255) DEFAULT NULL,
  `Latitude` float DEFAULT NULL,
  `Longitude` float DEFAULT NULL,
  PRIMARY KEY (`LocationId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `roles` (
  `RoleId` char(39) NOT NULL,
  `Role` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`RoleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `ships` (
  `ShipId` char(39) NOT NULL,
  `ShipName` varchar(45) DEFAULT NULL,
  `BuildDate` datetime DEFAULT NULL,
  `Notes` varchar(255) DEFAULT NULL,
  `ShipType` varchar(45) DEFAULT NULL,
  `Size` varchar(45) DEFAULT NULL,
  `OwnerBusinessId` char(39) DEFAULT NULL,
  `HomePortLocationId` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ShipId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `transactionhumans` (
  `TransactionId` char(39) NOT NULL,
  `HumanId` char(39) NOT NULL,
  `Notes` text,
  `Price` float DEFAULT NULL,
  PRIMARY KEY (`TransactionId`,`HumanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `transactions` (
  `TransactionId` char(39) NOT NULL,
  `TransactionDate` datetime DEFAULT NULL,
  `FromBusinessId` char(39) DEFAULT NULL,
  `ToBusinessId` char(39) DEFAULT NULL,
  `TransactionType` varchar(45) DEFAULT NULL,
  `Notes` text,
  `Act` varchar(155) DEFAULT NULL,
  `Page` varchar(155) DEFAULT NULL,
  `NotaryBusinessId` char(39) DEFAULT NULL,
  `Volume` varchar(155) DEFAULT NULL,
  `URL` varchar(255) DEFAULT NULL,
  `NeedsReview` int DEFAULT NULL,
  `TranscriberUserId` char(39) DEFAULT NULL,
  `TotalPrice` float DEFAULT NULL,
  `FromLocationId` char(39) DEFAULT NULL,
  `ToLocationId` char(39) DEFAULT NULL,
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

CREATE TABLE `voyagehumans` (
  `VoyageId` char(39) NOT NULL,
  `HumanId` char(39) NOT NULL,
  `RoleId` char(39) DEFAULT NULL,
  `Notes` varchar(255) DEFAULT NULL,
  `OwnerStartBusinessId` char(39) DEFAULT NULL,
  `OwnerEndBusinessId` char(39) DEFAULT NULL,
  `ShippingAgentBusinessId` char(39) DEFAULT NULL,
  PRIMARY KEY (`VoyageId`,`HumanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `voyages` (
  `VoyageId` char(39) NOT NULL,
  `ShipId` char(39) DEFAULT NULL,
  `CaptainHumanId` char(39) DEFAULT NULL,
  `StartLocationId` char(39) DEFAULT NULL,
  `EndLocationId` char(39) DEFAULT NULL,
  `StartDate` datetime DEFAULT NULL,
  `EndDate` datetime DEFAULT NULL,
  `Notes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`VoyageId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



CREATE USER 'developer'@'localhost' IDENTIFIED BY 'developer';
GRANT ALL PRIVILEGES ON *.* TO 'developer'@'localhost' WITH GRANT OPTION;
