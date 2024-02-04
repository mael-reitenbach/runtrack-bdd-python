BEGIN;
DELETE FROM etudiant WHERE id = 3;
SET @num := 0;
UPDATE etudiant SET id = @num := (@num+1);
ALTER TABLE etudiant AUTO_INCREMENT = 1;
COMMIT;
