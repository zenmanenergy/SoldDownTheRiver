-- Create humansarchive table to store merged/archived human records
CREATE TABLE IF NOT EXISTS `humansarchive` (
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
