-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema shelter_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema shelter_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `shelter_db` DEFAULT CHARACTER SET utf8 ;
USE `shelter_db` ;

-- -----------------------------------------------------
-- Table `shelter_db`.`shelters`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `shelter_db`.`shelters` (
  `shelter_id` INT NOT NULL AUTO_INCREMENT,
  `shelter_name` VARCHAR(60) NOT NULL,
  `city` VARCHAR(40) NOT NULL,
  `street` VARCHAR(40) NOT NULL,
  `zip` CHAR(5) NOT NULL,
  `phone` CHAR(10) NOT NULL,
  `email` VARCHAR(80) NULL,
  PRIMARY KEY (`shelter_id`))
ENGINE = InnoDB;

CREATE INDEX `idx_city_zip` ON `shelter_db`.`shelters` (`city` ASC, `zip` ASC) VISIBLE;

CREATE UNIQUE INDEX `uq_email` ON `shelter_db`.`shelters` (`email` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `shelter_db`.`animals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `shelter_db`.`animals` (
  `animal_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(40) NOT NULL,
  `species` ENUM('DOG', 'CAT') NOT NULL,
  `size` ENUM('Small', 'Medium', 'Large') NOT NULL,
  `hypoallergenic` ENUM('YES', 'NO') NOT NULL,
  `breed` VARCHAR(40) NULL,
  `sex` ENUM('Male', 'Female') NOT NULL,
  `date_of_birth` DATE NULL,
  `intake_date` DATE NOT NULL,
  `status` ENUM('Available', 'Adopted', 'Foster', 'Pending') NOT NULL,
  `shelter_id` INT NOT NULL,
  PRIMARY KEY (`animal_id`),
  CONSTRAINT `fk_animals-shelters`
    FOREIGN KEY (`shelter_id`)
    REFERENCES `shelter_db`.`shelters` (`shelter_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_animals-shelters_idx` ON `shelter_db`.`animals` (`shelter_id` ASC) VISIBLE;

CREATE INDEX `idx_species` ON `shelter_db`.`animals` (`species` ASC) VISIBLE;

CREATE INDEX `idx_status` ON `shelter_db`.`animals` (`status` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `shelter_db`.`employees`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `shelter_db`.`employees` (
  `employee_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(40) NOT NULL,
  `last_name` VARCHAR(40) NOT NULL,
  `role` ENUM('Manager', 'Vet Tech', 'Vet Assistant', 'Animal Assistant', 'Animal Caretaker', 'Groomer', 'Volunteer Coordinator') NOT NULL,
  `phone` CHAR(10) NULL,
  `email` VARCHAR(80) NULL,
  `shelter_id` INT NOT NULL,
  PRIMARY KEY (`employee_id`),
  CONSTRAINT `fk_employees_shelters`
    FOREIGN KEY (`shelter_id`)
    REFERENCES `shelter_db`.`shelters` (`shelter_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_employees_shelters_idx` ON `shelter_db`.`employees` (`shelter_id` ASC) VISIBLE;

CREATE UNIQUE INDEX `uniq_email` ON `shelter_db`.`employees` (`email` ASC) VISIBLE;

CREATE INDEX `idx_role` ON `shelter_db`.`employees` (`role` ASC) VISIBLE;

CREATE INDEX `idx_shelter_role` ON `shelter_db`.`employees` (`shelter_id` ASC, `role` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `shelter_db`.`vaccines`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `shelter_db`.`vaccines` (
  `vaccine_id` INT NOT NULL AUTO_INCREMENT,
  `vaccine_name` VARCHAR(40) NOT NULL,
  `species` ENUM('DOG', 'CAT') NOT NULL,
  `quantity` INT NOT NULL DEFAULT 0,
  `notes` TEXT(80) NULL,
  PRIMARY KEY (`vaccine_id`))
ENGINE = InnoDB;

CREATE INDEX `idx_vaccines_species` ON `shelter_db`.`vaccines` (`species` ASC) VISIBLE;

CREATE UNIQUE INDEX `idx_vaccine_name` ON `shelter_db`.`vaccines` (`vaccine_name` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `shelter_db`.`vaccination_record`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `shelter_db`.`vaccination_record` (
  `vaccination_id` INT NOT NULL AUTO_INCREMENT,
  `animal_id` INT NOT NULL,
  `vaccine_id` INT NOT NULL,
  `employee_id` INT NOT NULL,
  `vaccination_date` DATE NOT NULL,
  `due_date` DATE NOT NULL,
  `notes` TEXT(80) NULL,
  PRIMARY KEY (`vaccination_id`),
  CONSTRAINT `fk_vacc_animal`
    FOREIGN KEY (`animal_id`)
    REFERENCES `shelter_db`.`animals` (`animal_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_vacc_vaccine`
    FOREIGN KEY (`vaccine_id`)
    REFERENCES `shelter_db`.`vaccines` (`vaccine_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_vacc_employee`
    FOREIGN KEY (`employee_id`)
    REFERENCES `shelter_db`.`employees` (`employee_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_vacc_animal_idx` ON `shelter_db`.`vaccination_record` (`animal_id` ASC) VISIBLE;

CREATE INDEX `fk_vacc_employee_idx` ON `shelter_db`.`vaccination_record` (`employee_id` ASC) VISIBLE;

CREATE INDEX `idx_due_date` ON `shelter_db`.`vaccination_record` (`due_date` ASC) VISIBLE;

CREATE INDEX `fk_vacc_vaccine` ON `shelter_db`.`vaccination_record` (`vaccine_id` ASC) VISIBLE;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table shelters
-- -----------------------------------------------------
INSERT INTO shelters
    (shelter_name, city, street, zip, phone, email)
VALUES
    ('Happy Paws','Miami','Main St','33154','3056767325','info@happypaws.org'),
    ('Friends and Kennels','Miami','Harding St','33140','3053645789','contact@friendskennels.org'),
    ('Bark and Friends','Coral Gables','Sunset Dr','33143','3055120985','hello@barkfriends.org'),
    ('Miami Rescue Center','Miami','Biscayne Blvd','33132','3059982233','info@mirescue.org'),
    ('Pinecrest Pet Haven','Pinecrest','Red Rd','33156','3058441982','team@pinecresthaven.org'),
    ('Kendall Pet Sanctuary','Kendall','SW 88th St','33176','3055524499','contact@kendallpets.org');

-- -----------------------------------------------------
-- Data for table animals
-- -----------------------------------------------------
INSERT INTO animals
    (name,species,size,hypoallergenic,breed,sex,date_of_birth,intake_date,status,shelter_id)
VALUES
    ('Bella','DOG','Medium','YES','Labrador Retriever','Female','2021-05-10','2024-03-01','Available',1),
    ('Max','DOG','Large','NO','German Shepherd Mix','Male',NULL,'2024-02-15','Available',2),
    ('Luna','CAT','Small','YES','Siamese','Female','2022-03-18','2024-04-10','Foster',3),
    ('Rocky','DOG','Medium','NO','Unknown','Male','2024-09-25','2024-01-20','Adopted',4),
    ('Milo','CAT','Small','NO','Domestic Shorthair','Male','2023-01-05','2024-05-02','Available',5),
    ('Daisy','DOG','Small','YES','Poodle Mix','Female',NULL,'2024-03-18','Pending',6),
    ('Charlie','DOG','Large','NO','Rottweiler','Male',NULL,'2024-02-28','Available',1),
    ('Pepper','CAT','Small','NO','Tabby','Female','2022-07-19','2024-04-25','Available',2),
    ('Oliver','DOG','Medium','NO','Mixed Breed','Male',NULL,'2024-03-30','Available',3),
    ('Nala','CAT','Small','YES','Russian Blue','Female','2023-02-11','2024-05-12','Foster',4),
    ('Simba','DOG','Medium','YES','Goldendoodle','Male','2022-10-05','2024-03-22','Available',5),
    ('Coco','DOG','Small','NO','Unknown','Female','2020-09-09','2024-01-10','Adopted',6);

-- -----------------------------------------------------
-- Data for table employees
-- -----------------------------------------------------
INSERT INTO employees
    (first_name,last_name,role,phone,email,shelter_id)
VALUES
    ('Emma','Carter','Manager','3051112233','ecarter@happypaws.org',1),
    ('Noah','Bennett','Animal Caretaker','3051118899','nbennett@happypaws.org',1),
    ('Chloe','Martin','Vet Tech',NULL,'cmartin@happypaws.org',1),
    ('Sophia','Mitchell','Manager','3052223344','smitchell@friendskennels.org',2),
    ('Liam','Turner','Vet Tech','3052224477','lturner@friendskennels.org',2),
    ('Grace','Owens','Animal Caretaker','3052225599','gowens@friendskennels.org',2),
    ('Olivia','Reed','Manager','3053335566','oreed@barkfriends.org',3),
    ('Ethan','Brooks','Vet Assistant','3053337788','ebrooks@barkfriends.org',3),
    ('Zoe','Hughes','Volunteer Coordinator','3053339911','zhughes@barkfriends.org',3),
    ('Ava','Hayes','Vet Tech','3054446677','ahayes@mirescue.org',4),
    ('Mason','Cole','Animal Caretaker','3054448899','mcole@mirescue.org',4),
    ('Nora','Price','Manager',NULL,'nprice@mirescue.org',4),
    ('Mia','Foster','Vet Assistant','7861112244','mfoster@pinecresthaven.org',5),
    ('Logan','Gray','Manager','7861115566','lgray@pinecresthaven.org',5),
    ('Harper','James','Manager','7862223344','hjames@kendallpets.org',6),
    ('Lucas','Parker','Vet Assistant','7869991122','lparker@kendallpets.org',6);

-- -----------------------------------------------------
-- Data for table vaccines
-- -----------------------------------------------------
INSERT INTO vaccines
    (vaccine_name,species,quantity,notes)
VALUES
('Rabies-Dog','DOG',80,'Required annually'),
('DHPP','DOG',60,'Distemper, Hepatitis, Parainfluenza, Parvovirus'),
('Bordetella','DOG',45,'Kennel cough vaccine'),
('Leptospirosis','DOG',30,'Optional based on area'),
('Canine Influenza','DOG',35,'Flu protection'),
('Rabies-Cat','CAT',70,'Annual core vaccine'),
('FVRCP','CAT',55,'Rhinotracheitis, Calicivirus, Panleukopenia'),
('FeLV','CAT',25,'Recommended for outdoor cats'),
('Chlamydia','CAT',15,'Optional depending on exposure'),
('FIP','CAT',10,'Experimental vaccine');

-- -----------------------------------------------------
-- Data for table vaccination_record
-- -----------------------------------------------------
INSERT INTO vaccination_record
    (animal_id,vaccine_id,employee_id,vaccination_date,due_date,notes)
VALUES
    ((SELECT animal_id FROM animals WHERE name='Bella'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Rabies-Dog'),
     (SELECT employee_id FROM employees WHERE first_name='Chloe' AND last_name='Martin'),
     '2024-03-10','2025-03-10','Initial rabies shot'),

    ((SELECT animal_id FROM animals WHERE name='Bella'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='DHPP'),
     (SELECT employee_id FROM employees WHERE first_name='Chloe' AND last_name='Martin'),
     '2024-03-17','2025-03-17','Core combo vaccine'),

    ((SELECT animal_id FROM animals WHERE name='Bella'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Bordetella'),
     (SELECT employee_id FROM employees WHERE first_name='Chloe' AND last_name='Martin'),
     '2024-03-24','2025-03-24','Kennel cough'),

    ((SELECT animal_id FROM animals WHERE name='Max'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Rabies-Dog'),
     (SELECT employee_id FROM employees WHERE first_name='Liam' AND last_name='Turner'),
     '2024-02-20','2025-02-20','Annual rabies shot'),

    ((SELECT animal_id FROM animals WHERE name='Max'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='DHPP'),
     (SELECT employee_id FROM employees WHERE first_name='Liam' AND last_name='Turner'),
     '2024-02-27','2025-02-27','Core combo vaccine'),

    ((SELECT animal_id FROM animals WHERE name='Luna'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Rabies-Cat'),
     (SELECT employee_id FROM employees WHERE first_name='Ethan' AND last_name='Brooks'),
     '2024-04-15','2025-04-15','Initial rabies for indoor cat'),

    ((SELECT animal_id FROM animals WHERE name='Luna'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='FVRCP'),
     (SELECT employee_id FROM employees WHERE first_name='Ethan' AND last_name='Brooks'),
     '2024-04-22','2025-04-22','Core vaccine'),

    ((SELECT animal_id FROM animals WHERE name='Rocky'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Rabies-Dog'),
     (SELECT employee_id FROM employees WHERE first_name='Ava' AND last_name='Hayes'),
     '2024-01-25','2025-01-25','Rabies for stray intake'),

    ((SELECT animal_id FROM animals WHERE name='Milo'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Rabies-Cat'),
     (SELECT employee_id FROM employees WHERE first_name='Mia' AND last_name='Foster'),
     '2024-05-05','2025-05-05','Core rabies'),

    ((SELECT animal_id FROM animals WHERE name='Milo'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='FeLV'),
     (SELECT employee_id FROM employees WHERE first_name='Mia' AND last_name='Foster'),
     '2024-05-12','2025-05-12','Outdoor cat leukemia vaccine'),

    ((SELECT animal_id FROM animals WHERE name='Daisy'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Rabies-Dog'),
     (SELECT employee_id FROM employees WHERE first_name='Lucas' AND last_name='Parker'),
     '2024-03-22','2025-03-22','Rabies for small dog'),

    ((SELECT animal_id FROM animals WHERE name='Daisy'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Bordetella'),
     (SELECT employee_id FROM employees WHERE first_name='Lucas' AND last_name='Parker'),
     '2024-03-29','2025-03-29','Boarding requirement'),

    ((SELECT animal_id FROM animals WHERE name='Charlie'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Rabies-Dog'),
     (SELECT employee_id FROM employees WHERE first_name='Chloe' AND last_name='Martin'),
     '2024-03-02','2025-03-02','Rabies for large dog'),

    ((SELECT animal_id FROM animals WHERE name='Charlie'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Canine Influenza'),
     (SELECT employee_id FROM employees WHERE first_name='Chloe' AND last_name='Martin'),
     '2024-03-09','2025-03-09','Flu vaccine'),

    ((SELECT animal_id FROM animals WHERE name='Pepper'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Rabies-Cat'),
     (SELECT employee_id FROM employees WHERE first_name='Liam' AND last_name='Turner'),
     '2024-04-28','2025-04-28','Core rabies'),

    ((SELECT animal_id FROM animals WHERE name='Pepper'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='FVRCP'),
     (SELECT employee_id FROM employees WHERE first_name='Liam' AND last_name='Turner'),
     '2024-05-05','2025-05-05','Core combo vaccine'),

    ((SELECT animal_id FROM animals WHERE name='Oliver'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Rabies-Dog'),
     (SELECT employee_id FROM employees WHERE first_name='Ethan' AND last_name='Brooks'),
     '2024-04-03','2025-04-03','Initial rabies shot'),

    ((SELECT animal_id FROM animals WHERE name='Oliver'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Bordetella'),
     (SELECT employee_id FROM employees WHERE first_name='Ethan' AND last_name='Brooks'),
     '2024-04-10','2025-04-10','Kennel cough booster'),

    ((SELECT animal_id FROM animals WHERE name='Nala'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Rabies-Cat'),
     (SELECT employee_id FROM employees WHERE first_name='Ava' AND last_name='Hayes'),
     '2024-05-15','2025-05-15','Core rabies'),

    ((SELECT animal_id FROM animals WHERE name='Nala'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='FVRCP'),
     (SELECT employee_id FROM employees WHERE first_name='Ava' AND last_name='Hayes'),
     '2024-05-22','2025-05-22','Core combo'),

    ((SELECT animal_id FROM animals WHERE name='Nala'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Chlamydia'),
     (SELECT employee_id FROM employees WHERE first_name='Ava' AND last_name='Hayes'),
     '2024-05-29','2025-05-29','Extra protection due to exposure'),

    ((SELECT animal_id FROM animals WHERE name='Simba'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Rabies-Dog'),
     (SELECT employee_id FROM employees WHERE first_name='Mia' AND last_name='Foster'),
     '2024-03-26','2025-03-26','Core rabies'),

    ((SELECT animal_id FROM animals WHERE name='Simba'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='DHPP'),
     (SELECT employee_id FROM employees WHERE first_name='Mia' AND last_name='Foster'),
     '2024-04-03','2025-04-03','Core combo'),

    ((SELECT animal_id FROM animals WHERE name='Simba'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Leptospirosis'),
     (SELECT employee_id FROM employees WHERE first_name='Mia' AND last_name='Foster'),
     '2024-04-09','2025-04-09','Lepto for hiking dog'),

    ((SELECT animal_id FROM animals WHERE name='Coco'),
     (SELECT vaccine_id FROM vaccines WHERE vaccine_name='Rabies-Cat'),
     (SELECT employee_id FROM employees WHERE first_name='Lucas' AND last_name='Parker'),
     '2024-01-15','2025-01-15','Senior cat core rabies');
 
-- ============================================
-- FINAL VALIDATION QUERIES
-- ============================================

SHOW TABLES; 
SELECT COUNT(*) AS shelters FROM shelters;
SELECT COUNT(*) AS animals FROM animals;
SELECT COUNT(*) AS employees FROM employees;
SELECT COUNT(*) AS vaccines FROM vaccines;
SELECT COUNT(*) AS vaccination_records FROM vaccination_record;

SELECT * FROM shelters;
SELECT * FROM animals; 
SELECT * FROM employees;
SELECT * FROM vaccines;
SELECT * FROM vaccination_record; 






