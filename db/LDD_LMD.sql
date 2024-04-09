USE MASTER;

GO
IF DB_ID('LDDProject') IS NOT NULL

ALTER DATABASE LDDPROJECT SET SINGLE_USER WITH ROLLBACK IMMEDIATE;

GO

DROP DATABASE IF EXISTS LDDPROJECT;

GO

CREATE DATABASE LDDPROJECT;

GO
USE LDDPROJECT;

GO

DROP TABLE IF EXISTS MOTSINDEXFICHIER;

DROP TABLE IF EXISTS MEMBRERECHERCHEFICHIER;

DROP TABLE IF EXISTS MEMBREVISUALISEFICHIER;

DROP TABLE IF EXISTS INTERNAUTERECHERCHEFICHIER;

DROP TABLE IF EXISTS FICHIER;

DROP TABLE IF EXISTS MOTCLE;

DROP TABLE IF EXISTS MEMBRE;

DROP TABLE IF EXISTS THEME;

DROP TABLE IF EXISTS ADMINISTRATEUR;

CREATE TABLE ADMINISTRATEUR (
    ADMIN_ID INT PRIMARY KEY,
    NOM VARCHAR(255) NOT NULL,
    PRENOM VARCHAR(255) NOT NULL,
    EMAIL VARCHAR(255) UNIQUE NOT NULL,
    MOT_DE_PASS VARCHAR(255) NOT NULL
);

CREATE TABLE THEME (
    THEMEID INT PRIMARY KEY,
    NOM VARCHAR(255) NOT NULL,
    DESCRIPTION TEXT
);

CREATE TABLE MEMBRE (
    MEMBRE_ID INT PRIMARY KEY,
    PSEUDO VARCHAR(255) UNIQUE NOT NULL,
    EMAIL VARCHAR(255) UNIQUE NOT NULL,
    DATENAISSANCE DATE NOT NULL,
    NOM VARCHAR(255) NOT NULL,
    PRENOM VARCHAR(255) NOT NULL,
    MOTDEPASSE VARCHAR(255) NOT NULL,
    IMAGEPROFIL VARCHAR(255)
);

CREATE TABLE FICHIER (
    FICHIER_ID INT PRIMARY KEY,
    TYPE VARCHAR(255) NOT NULL,
    CHEMIN VARCHAR(255) NOT NULL,
    DESCRIPTION TEXT NOT NULL,
    DATEUPLOAD DATETIME2 NOT NULL,
    THEMEID INT NOT NULL,
    MEMBREID INT NOT NULL,
    FOREIGN KEY (THEMEID) REFERENCES THEME(THEMEID),
    FOREIGN KEY (MEMBREID) REFERENCES MEMBRE(MEMBRE_ID)
);

CREATE TABLE MOTCLE (
    MOTCLEID INT PRIMARY KEY,
    MOTCLE VARCHAR(255) NOT NULL
);

CREATE TABLE INTERNAUTERECHERCHEFICHIER (
    FICHIER_ID INT NOT NULL,
    PRIMARY KEY (FICHIER_ID),
    FOREIGN KEY (FICHIER_ID) REFERENCES FICHIER(FICHIER_ID)
);

CREATE TABLE MEMBREVISUALISEFICHIER (
    FICHIER_ID INT NOT NULL,
    MEMBRE_ID INT NOT NULL,
    PRIMARY KEY (FICHIER_ID, MEMBRE_ID),
    FOREIGN KEY (FICHIER_ID) REFERENCES FICHIER(FICHIER_ID),
    FOREIGN KEY (MEMBRE_ID) REFERENCES MEMBRE(MEMBRE_ID)
);

CREATE TABLE MEMBRERECHERCHEFICHIER (
    FICHIER_ID INT NOT NULL,
    MEMBRE_ID INT NOT NULL,
    PRIMARY KEY (FICHIER_ID, MEMBRE_ID),
    FOREIGN KEY (FICHIER_ID) REFERENCES FICHIER(FICHIER_ID),
    FOREIGN KEY (MEMBRE_ID) REFERENCES MEMBRE(MEMBRE_ID)
);

CREATE TABLE MOTSINDEXFICHIER (
    MOTCLEID INT NOT NULL,
    FICHIER_ID INT NOT NULL,
    PRIMARY KEY (MOTCLEID, FICHIER_ID),
    FOREIGN KEY (MOTCLEID) REFERENCES MOTCLE(MOTCLEID),
    FOREIGN KEY (FICHIER_ID) REFERENCES FICHIER(FICHIER_ID)
);

INSERT INTO ADMINISTRATEUR(
    ADMIN_ID,
    NOM,
    PRENOM,
    EMAIL,
    MOT_DE_PASS
) VALUES (
    1,
    'Dupont',
    'Jean',
    'jeandupont@email.com',
    'password123'
),
(
    2,
    'Martin',
    'Alice',
    'alice.martin@email.com',
    'password456'
) INSERT INTO THEME (
    THEMEID,
    NOM,
    [DESCRIPTION]
) VALUES (
    1,
    'Romance',
    'Exploration des nuances de l’amour et des relations'
),
(
    2,
    'Action',
    'Aventure a couper le souffle'
),
(
    3,
    'Musique',
    'Classique au moderne '
),
(
    4,
    'Drama',
    'Des recit intenses'
),
(
    5,
    'Horreur',
    'Frissonsgarantis avec des histoires'
),
(
    6,
    'Comedy',
    'Pour un bon moment de rire'
),
(
    7,
    'Science Fiction',
    'Exploration'
),
(
    8,
    'Mystère',
    'Enquêtes et secrets à résoudre dans un brouillard d’intrigues'
);

INSERT INTO MEMBRE(
    MEMBRE_ID,
    PSEUDO,
    EMAIL,
    DATENAISSANCE,
    NOM,
    PRENOM,
    MOTDEPASSE,
    IMAGEPROFIL
) VALUES (
    1,
    'TechGuru',
    'tech.guru@email.com',
    '1985-04-12',
    'Leroy',
    'Maxime',
    'securePass1',
    'profil1.jpg'
),
(
    2,
    'NatureLover',
    'nature.lover@email.com',
    '1992-07-25',
    'Bernard',
    'Léa',
    'securePass2',
    'profil2.jpg'
),
(
    3,
    'RomanceReader',
    'romance.reader@email.com',
    '1990-06-15',
    'Moreau',
    'Claire',
    'securePass3',
    'profil3.jpg'
),
(
    4,
    'ActionFan',
    'action.fan@email.com',
    '1988-11-03',
    'Petit',
    'Lucas',
    'securePass4',
    'profil4.jpg'
),
(
    5,
    'MusicMaven',
    'music.maven@email.com',
    '1995-02-20',
    'Garcia',
    'Emma',
    'securePass5',
    'profil5.jpg'
),
(
    6,
    'DramaQueen',
    'drama.queen@email.com',
    '1987-09-30',
    'Roux',
    'Sophie',
    'securePass6',
    'profil6.jpg'
),
(
    7,
    'HorrorBuff',
    'horror.buff@email.com',
    '1993-08-13',
    'Vincent',
    'Hugo',
    'securePass7',
    'profil7.jpg'
),
(
    8,
    'ComedyKing',
    'comedy.king@email.com',
    '1989-04-25',
    'Lefebvre',
    'Alexandre',
    'securePass8',
    'profil8.jpg'
),
(
    9,
    'SciFiNerd',
    'scifi.nerd@email.com',
    '1994-12-05',
    'Mercier',
    'Julien',
    'securePass9',
    'profil9.jpg'
),
(
    10,
    'MysterySleuth',
    'mystery.sleuth@email.com',
    '1986-03-17',
    'Dupuis',
    'Marie',
    'securePass10',
    'profil10.jpg'
);

INSERT INTO FICHIER (
    FICHIER_ID,
    TYPE,
    CHEMIN,
    DESCRIPTION,
    DATEUPLOAD,
    THEMEID,
    MEMBREID
) VALUES (
    1,
    'video',
    'documents/tech_trends.pdf',
    'Tendances technologiques 2024',
    '2024-01-15',
    1,
    1
),
(
    2,
    'jpg',
    'images/nature_forest.jpg',
    'Forêt mystique en automne',
    '2024-02-20',
    2,
    2
);

INSERT INTO MOTCLE (
    MOTCLEID,
    MOTCLE
) VALUES (
    1,
    'Innovation'
),
(
    2,
    'Écologie'
);

INSERT INTO INTERNAUTERECHERCHEFICHIER (
    FICHIER_ID
) VALUES (
    1
),
(
    2
);

INSERT INTO MEMBREVISUALISEFICHIER (
    FICHIER_ID,
    MEMBRE_ID
) VALUES (
    1,
    2
),
(
    2,
    1
);

INSERT INTO MEMBRERECHERCHEFICHIER (
    FICHIER_ID,
    MEMBRE_ID
) VALUES (
    1,
    2
),
(
    2,
    1
);

INSERT INTO MOTSINDEXFICHIER (
    MOTCLEID,
    FICHIER_ID
) VALUES (
    1,
    1
),
(
    2,
    2
);