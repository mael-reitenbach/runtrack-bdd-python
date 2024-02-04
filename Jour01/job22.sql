 SELECT * FROM etudiant WHERE age = (SELECT MIN(age) FROM etudiant);
