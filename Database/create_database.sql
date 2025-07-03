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

CREATE TABLE `humanclosure` (
  `AncestorHumanId` char(39) NOT NULL,
  `DescendantHumanId` char(39) NOT NULL,
  `Depth` int DEFAULT NULL,
  `DateUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`AncestorHumanId`,`DescendantHumanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `humanrelationships` (
  `ParentHumanId` char(39) NOT NULL,
  `ChildHumanId` char(39) NOT NULL,
  `DateUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`ParentHumanId`,`ChildHumanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `humanroles` (
  `HumanId` char(39) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `RoleId` char(39) NOT NULL,
  `date_circa` date DEFAULT NULL,
  `date_accuracy` char(1) DEFAULT NULL,
  `DateUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`HumanId`,`RoleId`),
  KEY `roleid` (`RoleId`,`HumanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `humans` (
  `HumanId` char(39) NOT NULL,
  `FirstName` varchar(255) DEFAULT NULL,
  `MiddleName` varchar(255) DEFAULT NULL,
  `LastName` varchar(155) DEFAULT NULL,
  `isCompany` varchar(2) DEFAULT NULL,
  `Notes` text,
  `age_string` varchar(45) DEFAULT NULL,
  `BirthDate` datetime DEFAULT NULL,
  `BirthDateAccuracy` varchar(45) DEFAULT NULL,
  `BirthPlace` varchar(45) DEFAULT NULL,
  `RacialDescriptor` char(39) DEFAULT NULL,
  `Sex` varchar(45) DEFAULT NULL,
  `Height_cm` double DEFAULT NULL,
  `DateUpdated` datetime DEFAULT NULL,
  `originCity` varchar(45) DEFAULT NULL,
  `physical_features` varchar(45) DEFAULT NULL,
  `profession` varchar(45) DEFAULT NULL,
  `mergedHumanId` char(39) DEFAULT NULL,
  `spouseHumanId` char(39) DEFAULT NULL,
  `swap_FirstName` varchar(255) DEFAULT NULL,
  `swap_LastName` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`HumanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `humans_backup` (
  `HumanId` char(39) NOT NULL,
  `FirstName` varchar(255) DEFAULT NULL,
  `MiddleName` varchar(255) DEFAULT NULL,
  `LastName` varchar(155) DEFAULT NULL,
  `Notes` text,
  `age_string` varchar(45) DEFAULT NULL,
  `BirthDate` datetime DEFAULT NULL,
  `BirthDateAccuracy` varchar(45) DEFAULT NULL,
  `BirthPlace` varchar(45) DEFAULT NULL,
  `RacialDescriptor` char(39) DEFAULT NULL,
  `Sex` varchar(45) DEFAULT NULL,
  `Height_cm` double DEFAULT NULL,
  `DateUpdated` datetime DEFAULT NULL,
  `originCity` varchar(45) DEFAULT NULL,
  `physical_features` varchar(45) DEFAULT NULL,
  `profession` varchar(45) DEFAULT NULL,
  `mergedHumanId` char(39) DEFAULT NULL,
  `spouseHumanId` char(39) DEFAULT NULL,
  PRIMARY KEY (`HumanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `humansarchive` (
  `HumanId` char(39) NOT NULL,
  `FirstName` varchar(255) DEFAULT NULL,
  `MiddleName` varchar(255) DEFAULT NULL,
  `LastName` varchar(155) DEFAULT NULL,
  `isCompany` varchar(2) DEFAULT NULL,
  `Notes` text,
  `age_string` varchar(45) DEFAULT NULL,
  `BirthDate` datetime DEFAULT NULL,
  `BirthDateAccuracy` varchar(45) DEFAULT NULL,
  `BirthPlace` varchar(45) DEFAULT NULL,
  `RacialDescriptor` char(39) DEFAULT NULL,
  `Sex` varchar(45) DEFAULT NULL,
  `Height_cm` double DEFAULT NULL,
  `DateUpdated` datetime DEFAULT NULL,
  `originCity` varchar(45) DEFAULT NULL,
  `physical_features` varchar(45) DEFAULT NULL,
  `profession` varchar(45) DEFAULT NULL,
  `mergedHumanId` char(39) DEFAULT NULL,
  `spouseHumanId` char(39) DEFAULT NULL,
  `swap_FirstName` varchar(255) DEFAULT NULL,
  `swap_LastName` varchar(255) DEFAULT NULL,
  `DateArchived` datetime DEFAULT NULL,
  PRIMARY KEY (`HumanId`),
  KEY `merged_human_idx` (`mergedHumanId`),
  KEY `date_archived_idx` (`DateArchived`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `humansaka` (
  `AKAHumanId` char(39) NOT NULL,
  `HumanId` char(39) NOT NULL,
  `AKAFirstName` varchar(45) DEFAULT NULL,
  `AKAMiddleName` varchar(45) DEFAULT NULL,
  `AKALastName` varchar(45) DEFAULT NULL,
  `DateUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`AKAHumanId`),
  KEY `human` (`HumanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `humantimeline` (
  `HumanId` char(39) NOT NULL,
  `LocationId` char(39) NOT NULL,
  `Date_Circa` date NOT NULL,
  `Date_Accuracy` varchar(1) NOT NULL,
  `LocationType` varchar(255) DEFAULT NULL,
  `RoleId` char(39) DEFAULT NULL,
  `DateUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`HumanId`,`LocationId`,`Date_Circa`,`Date_Accuracy`),
  KEY `location` (`LocationId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `locationaddresses` (
  `LocationId` char(39) NOT NULL,
  `Address` varchar(255) NOT NULL,
  `DateUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`LocationId`,`Address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `locations` (
  `LocationId` char(39) NOT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `City` varchar(255) DEFAULT NULL,
  `County` varchar(255) DEFAULT NULL,
  `State` varchar(255) DEFAULT NULL,
  `State_abbr` varchar(45) DEFAULT NULL,
  `Country` varchar(255) DEFAULT NULL,
  `Latitude` decimal(10,6) DEFAULT NULL,
  `Longitude` decimal(10,6) DEFAULT NULL,
  `LocationType` varchar(45) DEFAULT NULL,
  `DateUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`LocationId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `raw_manifest` (
  `Manifest_ID` char(39) NOT NULL,
  `Timestamp` datetime DEFAULT NULL,
  `LastName` varchar(155) DEFAULT NULL,
  `FirstNameMiddleName` varchar(155) DEFAULT NULL,
  `Sex` varchar(45) DEFAULT NULL,
  `Age` varchar(45) DEFAULT NULL,
  `Height_feet` varchar(45) DEFAULT NULL,
  `Height_inches` varchar(45) DEFAULT NULL,
  `Color` varchar(45) DEFAULT NULL,
  `OwnersName` varchar(155) DEFAULT NULL,
  `OwnersLocation` varchar(155) DEFAULT NULL,
  `ShippingAgent` varchar(155) DEFAULT NULL,
  `ShippingAgentLocation` varchar(155) DEFAULT NULL,
  `Owner2` varchar(255) DEFAULT NULL,
  `Owner2Location` varchar(255) DEFAULT NULL,
  `ShipName` varchar(45) DEFAULT NULL,
  `ShipSize` varchar(45) DEFAULT NULL,
  `ShipType` varchar(45) DEFAULT NULL,
  `ShipCaptain` varchar(45) DEFAULT NULL,
  `ShipHomePort` varchar(45) DEFAULT NULL,
  `YearNorfolk` varchar(45) DEFAULT NULL,
  `MonthDayNorfolk` varchar(45) DEFAULT NULL,
  `DateNorfolk` datetime DEFAULT NULL,
  `CollectorAgent` varchar(155) DEFAULT NULL,
  `YearNOLA` varchar(45) DEFAULT NULL,
  `MonthDayNOLA` varchar(45) DEFAULT NULL,
  `DateNOLA` datetime DEFAULT NULL,
  `Notes` text,
  `Transcribers` varchar(155) DEFAULT NULL,
  `shipVoyageId` varchar(45) DEFAULT NULL,
  `teamNumber` varchar(155) DEFAULT NULL,
  `ReferenceScan` varchar(155) DEFAULT NULL,
  `SecondReference` varchar(1024) DEFAULT NULL,
  `valuation` varchar(155) DEFAULT NULL,
  `YearBalize` varchar(45) DEFAULT NULL,
  `MonthDayBalize` varchar(45) DEFAULT NULL,
  `NolasaleURL1` varchar(155) DEFAULT NULL,
  `FamilySearchURL1` varchar(155) DEFAULT NULL,
  `NOLA_date` date DEFAULT NULL,
  `Norfolk_date` date DEFAULT NULL,
  `balize_date` date DEFAULT NULL,
  `NOLA_date_accuracy` char(1) DEFAULT NULL,
  `Norfolk_date_accuracy` char(1) DEFAULT NULL,
  `Balize_date_accuracy` char(1) DEFAULT NULL,
  `NOLA_LocationId` char(39) DEFAULT NULL,
  `Norfolk_LocationId` char(39) DEFAULT NULL,
  `Balize_LocationId` char(39) DEFAULT NULL,
  `Owner_humanId` char(39) DEFAULT NULL,
  `ShippingAgent_humanId` char(39) DEFAULT NULL,
  `Owner_LocationId` char(39) DEFAULT NULL,
  `Owner2_humanId` char(39) DEFAULT NULL,
  `Owner2_LocationId` char(39) DEFAULT NULL,
  `CollectorAgent_humanId` char(39) DEFAULT NULL,
  `ShipId` char(39) DEFAULT NULL,
  `Captain_humanId` char(39) DEFAULT NULL,
  `shipHomePort_LocationId` char(39) DEFAULT NULL,
  `enslaved_humanid` char(39) DEFAULT NULL,
  `dateupdated` datetime DEFAULT NULL,
  PRIMARY KEY (`Manifest_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `raw_nola` (
  `NOLA_ID` char(39) NOT NULL,
  `Timestamp` datetime DEFAULT NULL,
  `FirstParty` varchar(250) DEFAULT NULL,
  `LocationFirstParty` varchar(100) DEFAULT NULL,
  `SecondParty` varchar(250) DEFAULT NULL,
  `LocationSecondParty` varchar(100) DEFAULT NULL,
  `TypeOfTransaction` varchar(100) DEFAULT NULL,
  `DateOfTransaction` varchar(100) DEFAULT NULL,
  `Act` varchar(100) DEFAULT NULL,
  `Page` varchar(100) DEFAULT NULL,
  `NotaryPublic` varchar(100) DEFAULT NULL,
  `Volume` varchar(100) DEFAULT NULL,
  `Notes` text,
  `Parsed_Notes` text,
  `Error_Notes` text,
  `ReferenceURL` varchar(255) DEFAULT NULL,
  `NameOfTranscriber` varchar(100) DEFAULT NULL,
  `LocationIdFirstParty` char(39) DEFAULT NULL,
  `LocationIdSecondParty` char(39) DEFAULT NULL,
  `SellerHumanId` char(39) DEFAULT NULL,
  `SellerResidenceLocationId` char(39) DEFAULT NULL,
  `BuyerHumanId` char(39) DEFAULT NULL,
  `BuyerResidenceLocationId` char(39) DEFAULT NULL,
  `NotaryHumanId` char(39) DEFAULT NULL,
  `Transaction_date` date DEFAULT NULL,
  PRIMARY KEY (`NOLA_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `reference` (
  `ReferenceId` char(39) NOT NULL,
  `URL` varchar(255) DEFAULT NULL,
  `Notes` varchar(255) DEFAULT NULL,
  `dateUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`ReferenceId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `referencelinks` (
  `ReferenceId` char(39) NOT NULL,
  `LinkId` char(39) NOT NULL,
  `TargetType` enum('voyage','transaction','human','ship') NOT NULL,
  `dateUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`ReferenceId`,`LinkId`,`TargetType`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `roles` (
  `RoleId` char(39) NOT NULL,
  `Role` varchar(45) DEFAULT NULL,
  `DateUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`RoleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `ships` (
  `ShipId` char(39) NOT NULL,
  `ShipName` varchar(45) DEFAULT NULL,
  `BuildDate` varchar(20) DEFAULT NULL,
  `Notes` varchar(255) DEFAULT NULL,
  `ShipType` varchar(45) DEFAULT NULL,
  `Size` varchar(45) DEFAULT NULL,
  `HomePortLocationId` varchar(45) DEFAULT NULL,
  `DateUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`ShipId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `transactionhumans` (
  `TransactionId` char(39) NOT NULL,
  `HumanId` char(39) NOT NULL,
  `RoleId` char(39) NOT NULL,
  `Notes` text,
  `ParsedNotes` text,
  `Price` float DEFAULT NULL,
  `originLocationId` char(39) DEFAULT NULL,
  `destinationLocationId` char(39) DEFAULT NULL,
  `DateUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`TransactionId`,`HumanId`,`RoleId`),
  KEY `Humans` (`HumanId`,`TransactionId`,`RoleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `transactions` (
  `TransactionId` char(39) NOT NULL,
  `date_circa` date DEFAULT NULL,
  `date_accuracy` char(1) DEFAULT NULL,
  `TransactionType` varchar(45) DEFAULT NULL,
  `Notes` text,
  `Act` varchar(155) DEFAULT NULL,
  `Page` varchar(155) DEFAULT NULL,
  `Volume` varchar(155) DEFAULT NULL,
  `URL` varchar(255) DEFAULT NULL,
  `NeedsReview` int DEFAULT NULL,
  `Transcriber` varchar(100) DEFAULT NULL,
  `NOLA_ID` char(39) DEFAULT NULL,
  `Parsed_Notes` text,
  `QuantityOfSlaves` int DEFAULT NULL,
  `TotalPrice` float DEFAULT NULL,
  `dataIssue` varchar(255) DEFAULT NULL,
  `Issues` text,
  `LocationId` char(39) DEFAULT NULL,
  `processedNotes` int DEFAULT NULL,
  `isApproved` int DEFAULT NULL,
  `DataQuestions` text,
  `DateUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`TransactionId`),
  KEY `nola_id` (`NOLA_ID`)
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
  `DateUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `usersessions` (
  `SessionId` char(39) NOT NULL,
  `UserId` char(39) NOT NULL,
  `DateAdded` datetime DEFAULT NULL,
  PRIMARY KEY (`UserId`,`SessionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `voyagehumans` (
  `VoyageId` char(39) NOT NULL,
  `HumanId` char(39) NOT NULL,
  `RoleId` char(39) DEFAULT NULL,
  `Notes` varchar(1024) DEFAULT NULL,
  `DateUpdated` datetime DEFAULT NULL,
  `manifest_id` char(39) DEFAULT NULL,
  `owner_humanid` char(39) DEFAULT NULL,
  `shippingagent_humanid` char(39) DEFAULT NULL,
  `owner2_humanid` char(39) DEFAULT NULL,
  `collectoragent_humanid` char(39) DEFAULT NULL,
  PRIMARY KEY (`VoyageId`,`HumanId`),
  KEY `humans` (`HumanId`) /*!80000 INVISIBLE */,
  KEY `role` (`RoleId`,`HumanId`,`VoyageId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `voyagereference` (
  `VoyageId` char(39) NOT NULL,
  `ReferenceId` char(39) DEFAULT NULL,
  `dateUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`VoyageId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `voyages` (
  `VoyageId` char(39) NOT NULL,
  `ShipId` char(39) DEFAULT NULL,
  `manifest_id` char(39) DEFAULT NULL,
  `CaptainHumanId` char(39) DEFAULT NULL,
  `StartLocationId` char(39) DEFAULT NULL,
  `EndLocationId` char(39) DEFAULT NULL,
  `StartDate` date DEFAULT NULL,
  `EndDate` date DEFAULT NULL,
  `Notes` varchar(1024) DEFAULT NULL,
  `CustomsLocationId` char(39) DEFAULT NULL,
  `CustomsDate` date DEFAULT NULL,
  `DateUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`VoyageId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
