-- Table to store humans
CREATE TABLE Humans (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	spouse_id INT DEFAULT NULL,
	FOREIGN KEY (spouse_id) REFERENCES Humans(id)
);

-- Table to store families
CREATE TABLE Families (
	id INT AUTO_INCREMENT PRIMARY KEY,
	family_name VARCHAR(255) NOT NULL
);

-- Table to link humans to families with tree positions
CREATE TABLE FamilyMembers (
	id INT AUTO_INCREMENT PRIMARY KEY,
	human_id INT NOT NULL,
	family_id INT NOT NULL,
	left_value INT NOT NULL,    -- Position in the family tree, scoped to the family
	right_value INT NOT NULL,   -- Position in the family tree, scoped to the family
	FOREIGN KEY (human_id) REFERENCES Humans(id),
	FOREIGN KEY (family_id) REFERENCES Families(id)
);

-- Insert data into Humans table
INSERT INTO Humans (id, name, spouse_id) VALUES
-- Family 1
(1, 'John', 2),       -- Root
(2, 'Mary', 1),       -- Spouse of John
(3, 'Alice', NULL),   -- Child of John and Mary
(4, 'Peter', NULL),   -- Child of John and Mary
(5, 'Bob', NULL),     -- Grandchild of John and Mary

-- Family 2
(6, 'Tom', 7),        -- Root
(7, 'Jerry', 6),      -- Spouse of Tom
(8, 'Anna', NULL),    -- Child of Tom and Jerry

-- Family 3
(9, 'Mary', NULL);    -- Mary is also a child in Family 3

-- Insert data into Families table
INSERT INTO Families (id, family_name) VALUES
(1, 'Family 1'),
(2, 'Family 2'),
(3, 'Family 3');

-- Insert data into FamilyMembers table
INSERT INTO FamilyMembers (family_id, human_id, left_value, right_value) VALUES
-- Family 1
(1, 1, 1, 10),
(1, 2, 2, 5),
(1, 3, 3, 4),
(1, 4, 6, 9),
(1, 5, 7, 8),

-- Family 2
(2, 6, 1, 6),  -- Reset left/right values for Family 2
(2, 7, 2, 3),
(2, 8, 4, 5),

-- Family 3
(3, 9, 1, 2);  -- Reset left/right values for Family 3

-- Query to retrieve the full family for a given HumanId
SELECT
	h2.*,
	fm2.left_value,
	fm2.right_value
FROM FamilyMembers AS fm1
JOIN FamilyMembers AS fm2
	ON fm1.family_id = fm2.family_id
JOIN Humans AS h2
	ON fm2.human_id = h2.id
WHERE fm1.human_id = {HumanId}
ORDER BY fm2.left_value;

-- Query to retrieve the spouse of a given HumanId
SELECT
	h1.name AS person_name,
	h2.name AS spouse_name
FROM Humans AS h1
LEFT JOIN Humans AS h2
	ON h1.spouse_id = h2.id
WHERE h1.id = {HumanId};