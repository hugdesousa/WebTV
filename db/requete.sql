USE LDDPROJECT

--Requêtes simples
SELECT
    *
FROM
    MEMBRE;

SELECT
    *
FROM
    FICHIER
WHERE
    TYPE = 'jpg';

SELECT
    NOM,
    PRENOM,
    EMAIL
FROM
    ADMINISTRATEUR;

SELECT
    NOM,
    DESCRIPTION
FROM
    THEME;

SELECT
    *
FROM
    MOTCLE;

--Sélection des membres qui ont visualiser le fichier 2
SELECT
    M.PSEUDO,
    M.EMAIL
FROM
    MEMBRE                 M
    JOIN MEMBREVISUALISEFICHIER MVF
    ON M.MEMBRE_ID = MVF.MEMBRE_ID
WHERE
    MVF.FICHIER_ID = 2;

-- Sélection des fichiers qui ont été téléchargés par des membres agés de moins de 20 ans
SELECT
    F.*
FROM
    FICHIER F
    JOIN MEMBRE M
    ON F.MEMBREID = M.MEMBRE_ID
WHERE
    DATEDIFF(YEAR, M.DATENAISSANCE, GETDATE()) < 40;

--Sélections des fichiers qui ont le mot clé Écologie
SELECT
    F.*
FROM
    FICHIER          F
    JOIN MOTSINDEXFICHIER MIF
    ON F.FICHIER_ID = MIF.FICHIER_ID
    JOIN MOTCLE MC
    ON MIF.MOTCLEID = MC.MOTCLEID
WHERE
    MC.MOTCLE = 'Écologie';

--Sélections des membres qui ont recherché un fichier mais qui ne l'ont regardé
SELECT
    M.*
FROM
    MEMBRE                 M
    JOIN MEMBRERECHERCHEFICHIER MRF
    ON M.MEMBRE_ID = MRF.MEMBRE_ID
    LEFT JOIN MEMBREVISUALISEFICHIER MVF
    ON M.MEMBRE_ID = MVF.MEMBRE_ID
WHERE
    MVF.MEMBRE_ID IS NOT NULL;

--Sélection des thèmes avec le nombre total de fichiers associés à chaque thème (trie par ordre décroissant du nombre de fichiers) :
SELECT
    T.NOM            AS NOM_THEME,
    COUNT(F.THEMEID) AS NOMBRE_FICHIERS_ASSOCIÉS
FROM
    THEME   T
    LEFT JOIN FICHIER F
    ON T.THEMEID = F.THEMEID
GROUP BY
    T.NOM
ORDER BY
    NOMBRE_FICHIERS_ASSOCIÉS DESC;

--Permet de Trouver les videos de la mots cle
SELECT F.Chemin,F.Description FROM Fichier F
JOIN MotsIndexFichier MIF ON F.Fichier_ID = MIF.Fichier_ID
JOIN MOTCLE MK ON MIF.MotCleID = MK.MotCleID
WHERE MK.MotCle LIKE '%Musique%'
