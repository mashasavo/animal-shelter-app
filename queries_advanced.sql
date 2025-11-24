-- =========================================================
-- Advanced Queries & Features for shelter_db
-- Schema: shelters, animals, employees, vaccines, vaccination_record
-- Includes:
--   • Simple SELECT + ORDER BY
--   • JOINs
--   • Aggregation + GROUP BY + HAVING
--   • Subquery (max vaccinations)
--   • Window function (RANK)
--   • Recursive CTE
--   • View
--   • Transaction demo (commented as optional)
--   • Trigger (stock decrement)
-- =========================================================

USE shelter_db;

-- =========================================================
-- 1. Simple queries, aggregation, joins
-- =========================================================

-- 1. List all animals, ordered by intake date (newest first)
SELECT animal_id,
       name,
       species,
       breed,
       status,
       intake_date
FROM animals
ORDER BY intake_date DESC;

-- 2. List all available dogs at "Happy Paws"
SELECT a.animal_id,
       a.name,
       a.breed,
       a.size,
       a.status,
       s.shelter_name
FROM animals a
JOIN shelters s
  ON a.shelter_id = s.shelter_id
WHERE a.species = 'DOG'
  AND a.status = 'Available'
  AND s.shelter_name = 'Happy Paws';

-- 3. List all vaccines for cats, ordered by quantity (largest to smallest)
SELECT vaccine_id,
       vaccine_name,
       species,
       quantity
FROM vaccines
WHERE species = 'CAT'
ORDER BY quantity DESC;

-- 4. How many vaccinations per species (DOG vs CAT)
SELECT a.species,
       COUNT(vr.vaccination_id) AS total_vaccinations
FROM vaccination_record vr
JOIN animals a
  ON vr.animal_id = a.animal_id
GROUP BY a.species;

-- 5. Animals that are overdue for vaccination (due_date < today and still Available/Foster)
SELECT
    a.name,
    a.species,
    v.vaccine_name,
    vr.due_date,
    s.shelter_name
FROM vaccination_record vr
JOIN animals  a ON vr.animal_id  = a.animal_id
JOIN vaccines v ON vr.vaccine_id = v.vaccine_id
JOIN shelters s ON a.shelter_id  = s.shelter_id
WHERE vr.due_date < CURDATE()
  AND a.status IN ('Available', 'Foster')
ORDER BY vr.due_date;

-- 6. Animals with the highest number of vaccinations (using subquery)
SELECT
    a.animal_id,
    a.name,
    COUNT(vr.vaccination_id) AS vacc_count
FROM animals a
JOIN vaccination_record vr
  ON vr.animal_id = a.animal_id
GROUP BY a.animal_id, a.name
HAVING COUNT(vr.vaccination_id) = (
    SELECT MAX(cnt)
    FROM (
        SELECT COUNT(vr2.vaccination_id) AS cnt
        FROM animals a2
        JOIN vaccination_record vr2
          ON vr2.animal_id = a2.animal_id
        GROUP BY a2.animal_id
    ) AS t
);

-- =========================================================
-- 2. More advanced queries
-- =========================================================

-- 7. Rank shelters by number of dogs (1 = busiest)
SELECT
    s.shelter_name,
    COUNT(a.animal_id) AS dog_count,
    RANK() OVER (ORDER BY COUNT(a.animal_id) DESC) AS shelter_rank
FROM shelters s
LEFT JOIN animals a
       ON a.shelter_id = s.shelter_id
      AND a.species = 'DOG'
GROUP BY s.shelter_id, s.shelter_name
ORDER BY shelter_rank, s.shelter_name;

-- 8. Next 30 days calendar showing how many vaccinations are due each day
WITH RECURSIVE next_days AS (
    SELECT CURDATE() AS day
    UNION ALL
    SELECT DATE_ADD(day, INTERVAL 1 DAY)
    FROM next_days
    WHERE day < DATE_ADD(CURDATE(), INTERVAL 30 DAY)
)
SELECT
    d.day,
    COUNT(vr.vaccination_id) AS vaccinations_due
FROM next_days d
LEFT JOIN vaccination_record vr
       ON vr.due_date = d.day
GROUP BY d.day
ORDER BY d.day;

-- =========================================================
-- 3. View for clean joined report per animal
-- =========================================================

-- 9. Create a view with a clean joined report on each animal
DROP VIEW IF EXISTS vw_animal_vaccinations;

CREATE VIEW vw_animal_vaccinations AS
SELECT
    vr.vaccination_id,
    a.animal_id,
    a.name       AS animal_name,
    a.species,
    v.vaccine_name,
    e.first_name AS employee_first,
    e.last_name  AS employee_last,
    s.shelter_name,
    vr.vaccination_date,
    vr.due_date,
    vr.notes
FROM vaccination_record vr
JOIN animals   a ON vr.animal_id   = a.animal_id
JOIN vaccines  v ON vr.vaccine_id  = v.vaccine_id
JOIN employees e ON vr.employee_id = e.employee_id
JOIN shelters  s ON a.shelter_id   = s.shelter_id;

-- Example usage of the view:
SELECT *
FROM vw_animal_vaccinations
WHERE species = 'DOG';

-- =========================================================
-- 4. Transaction demo (optional – you decided NOT to run it)
--    Left here as documentation to show transaction logic.
-- =========================================================

/*
-- 10. Transaction demo: add a new vaccination for Bella.
-- Stock would be decremented automatically by trigger trg_decrement_vaccine_stock.

START TRANSACTION;

INSERT INTO vaccination_record (animal_id, vaccine_id, employee_id, vaccination_date, due_date, notes)
VALUES (
    (SELECT animal_id   FROM animals   WHERE name = 'Bella'),
    (SELECT vaccine_id  FROM vaccines  WHERE vaccine_name = 'DHPP'),
    (SELECT employee_id FROM employees WHERE first_name = 'Chloe' AND last_name = 'Martin'),
    '2024-06-01',
    '2025-06-01',
    'DHPP annual booster via transaction demo'
);

COMMIT;
*/

-- =========================================================
-- 5. Trigger: after inserting a vaccination record, decrement vaccine stock
--    (You ALREADY ran this in shelter_db – here for completeness.)
-- =========================================================

DROP TRIGGER IF EXISTS trg_decrement_vaccine_stock;

DELIMITER //

CREATE TRIGGER trg_decrement_vaccine_stock
AFTER INSERT ON vaccination_record
FOR EACH ROW
BEGIN
    UPDATE vaccines
    SET quantity = CASE
        WHEN quantity > 0 THEN quantity - 1
        ELSE 0
    END
    WHERE vaccine_id = NEW.vaccine_id;
END//

DELIMITER ;

-- Check triggers (optional)
SHOW TRIGGERS;








