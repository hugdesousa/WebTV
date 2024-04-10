USE master;
GO

IF DB_ID('LDDProject') IS NOT NULL
    ALTER DATABASE LDDProject SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
GO

DROP DATABASE IF EXISTS LDDProject;
GO

CREATE DATABASE LDDProject;
GO

USE LDDProject;
GO

DROP TABLE IF EXISTS MotsIndexFichier;
DROP TABLE IF EXISTS MembreRechercheFichier;
DROP TABLE IF EXISTS MembreVisualiseFichier;
DROP TABLE IF EXISTS InternauteRechercheFichier;
DROP TABLE IF EXISTS Fichier;
DROP TABLE IF EXISTS MOTCLE;
DROP TABLE IF EXISTS Membre;
DROP TABLE IF EXISTS Theme;
DROP TABLE IF EXISTS Administrateur;

CREATE TABLE Administrateur (
    Admin_ID INT PRIMARY KEY,
    Nom VARCHAR(255) NOT NULL,
    Prenom VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Mot_de_Pass VARCHAR(255) NOT NULL
);

CREATE TABLE Theme (
    ThemeID INT PRIMARY KEY,
    Nom VARCHAR(255) NOT NULL,
    Description TEXT
);

CREATE TABLE Membre (
    Membre_ID INT PRIMARY KEY,
    Pseudo VARCHAR(255) UNIQUE NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    DateNaissance VARCHAR(255) NOT NULL,
    Nom VARCHAR(255) NOT NULL,
    Prenom VARCHAR(255) NOT NULL,
    MotdePasse VARCHAR(255) NOT NULL,
    ImageProfil VARCHAR(255)
);

CREATE TABLE Fichier (
    Fichier_ID INT PRIMARY KEY,
    Type VARCHAR(255) NOT NULL,
    Chemin VARCHAR(255) NOT NULL,
    Description TEXT NOT NULL,
    DateUpload datetime2 NOT NULL,
    ThemeID INT NOT NULL,
    MembreID INT NOT NULL,
    FOREIGN KEY (ThemeID) REFERENCES Theme(ThemeID),
    FOREIGN KEY (MembreID) REFERENCES Membre(Membre_ID)
);

CREATE TABLE MOTCLE (
    MotCleID INT PRIMARY KEY,
    MotCle VARCHAR(255) NOT NULL
);

CREATE TABLE InternauteRechercheFichier (
    Fichier_ID INT NOT NULL,
    PRIMARY KEY (Fichier_ID),
    FOREIGN KEY (Fichier_ID) REFERENCES Fichier(Fichier_ID)
);

CREATE TABLE MembreVisualiseFichier (
    Fichier_ID INT NOT NULL,
    Membre_ID INT NOT NULL,
    PRIMARY KEY (Fichier_ID, Membre_ID),
    FOREIGN KEY (Fichier_ID) REFERENCES Fichier(Fichier_ID),
    FOREIGN KEY (Membre_ID) REFERENCES Membre(Membre_ID)
);

CREATE TABLE MembreRechercheFichier (
    Fichier_ID INT NOT NULL,
    Membre_ID INT NOT NULL,
    PRIMARY KEY (Fichier_ID, Membre_ID),
    FOREIGN KEY (Fichier_ID) REFERENCES Fichier(Fichier_ID),
    FOREIGN KEY (Membre_ID) REFERENCES Membre(Membre_ID)
);

CREATE TABLE MotsIndexFichier (
    MotCleID INT NOT NULL,
    Fichier_ID INT NOT NULL,
    PRIMARY KEY (MotCleID, Fichier_ID),
    FOREIGN KEY (MotCleID) REFERENCES MOTCLE(MotCleID),
    FOREIGN KEY (Fichier_ID) REFERENCES Fichier(Fichier_ID)
);

Insert INTO Administrateur(Admin_ID,Nom,Prenom,Email,Mot_de_Pass)
VALUES
     (1,'Dupont','Jean','jeandupont@email.com','password123'),
     (2,'Martin','Alice','alice.martin@email.com','password456')

INSERT INTO Theme (ThemeID,Nom,[Description])
VALUES
     (1,'Romance','Exploration des nuances de l’amour et des relations'),
     (2,'Action','Aventure a couper le souffle'),
     (3,'Musique','Classique au moderne '),
     (4,'Drama','Des recit intenses'),
     (5,'Horreur','Frissonsgarantis avec des histoires'),
     (6,'Comedy','Pour un bon moment de rire'),
     (7,'Science Fiction','Exploration'),
     (8,'Mystère', 'Enquêtes et secrets à résoudre dans un brouillard d’intrigues');

INSERT INTO Membre(Membre_ID,Pseudo,Email,DateNaissance,Nom,Prenom,MotdePasse,ImageProfil)
VALUES
     (1, 'h', 'tech.guru@email.com', '1985-04-12', 'Leroy', 'Maxime', 'h', 'profil1.jpg'),
     (2, 'NatureLover', 'nature.lover@email.com', '1992-07-25', 'Bernard', 'Léa', 'securePass2', 'profil2.jpg'),
     (3, 'RomanceReader', 'romance.reader@email.com', '1990-06-15', 'Moreau', 'Claire', 'securePass3', 'profil3.jpg'),
     (4, 'ActionFan', 'action.fan@email.com', '1988-11-03', 'Petit', 'Lucas', 'securePass4', 'profil4.jpg'),
     (5, 'MusicMaven', 'music.maven@email.com', '1995-02-20', 'Garcia', 'Emma', 'securePass5', 'profil5.jpg'),
     (6, 'DramaQueen', 'drama.queen@email.com', '1987-09-30', 'Roux', 'Sophie', 'securePass6', 'profil6.jpg'),
     (7, 'HorrorBuff', 'horror.buff@email.com', '1993-08-13', 'Vincent', 'Hugo', 'securePass7', 'profil7.jpg'),
     (8, 'ComedyKing', 'comedy.king@email.com', '1989-04-25', 'Lefebvre', 'Alexandre', 'securePass8', 'profil8.jpg'),
     (9, 'SciFiNerd', 'scifi.nerd@email.com', '1994-12-05', 'Mercier', 'Julien', 'securePass9', 'profil9.jpg'),
     (10,'MysterySleuth', 'mystery.sleuth@email.com', '1986-03-17', 'Dupuis', 'Marie', 'securePass10', 'profil10.jpg');

INSERT INTO Fichier (Fichier_ID, Type, Chemin, Description, DateUpload, ThemeID, MembreID)
VALUES
(1, 'png', '../src/images/Beyonce.png', 'Beyonce ', '2024-01-15', 5, 1),
(2, 'mp4', '../src/images/Beyonce.mp4', 'Beyonce ', '2024-01-15', 5, 1),
(3, 'png', '../src/images/JustinBieber.png', 'Justin Bieber', '2024-01-15', 5, 1),
(4, 'mp4', '../src/images/JustinBieber.mp4', 'Justin Bieber', '2024-01-15', 5, 1),
(5, 'png', '../src/images/KattyPerry.png', 'Katy Perry', '2024-01-15', 5, 1),
(6, 'mp4', '../src/images/KattyPerry.mp4', 'Katy Perry', '2024-01-15', 5, 1),
(7, 'png', '../src/images/Rihana.png', 'Rihana', '2024-01-15', 5, 1),
(8, 'mp4', '../src/images/Rihana.mp4', 'Rihana', '2024-01-15', 5, 1),
    
(9, 'png', '../src/images/chien.png', 'Chien', '2024-01-15', 3, 1),
(10, 'mp4', '../src/images/chien.mp4', 'Chien', '2024-01-15', 3, 1),
(11, 'png', '../src/images/Bebe.png', 'Bebe', '2024-01-15', 3, 1),
(12, 'mp4', '../src/images/Bebe.mp4', 'Bebe', '2024-01-15', 3, 1),
(13, 'png', '../src/images/Laugh.png', 'Laugh', '2024-01-15', 3, 1),
(14, 'mp4', '../src/images/Laugh.mp4', 'Laugh', '2024-01-15', 3, 1),
(15, 'png', '../src/images/Fails.png', 'Fails', '2024-01-15', 3, 1),
(16, 'mp4', '../src/images/Fails.mp4', 'Fails', '2024-01-15', 3, 1),

(17, 'png', '../src/images/News1.png', 'News1', '2024-01-15', 9, 1),
(18, 'png', '../src/images/News2.png', 'News2', '2024-01-15', 9, 1),
(19, 'png', '../src/images/News3.png', 'News3', '2024-01-15', 9, 1),
(20, 'png', '../src/images/News4.png', 'News4', '2024-01-15', 9, 1),
(21, 'mp4', '../src/images/News1.mp4', 'News1', '2024-01-15', 9, 1),
(22, 'mp4', '../src/images/News2.mp4', 'News2', '2024-01-15', 9, 1),
(23, 'png', '../src/images/News3.png', 'News3', '2024-01-15', 9, 1),
(24, 'mp4', '../src/images/News4.mp4', 'News4', '2024-01-15', 9, 1);

INSERT INTO MOTCLE (MotCleID, MotCle)
VALUES
(1, 'Romance'),
(2, 'Action'),
(3, 'Comedy'),
(4, 'Horreur'),
(5, 'Musique'),
(6, 'Science Fiction'),
(7, 'Drama'),
(8, 'Mystere'),
(9, 'News');


INSERT INTO InternauteRechercheFichier (Fichier_ID)
VALUES
(1),
(2);

INSERT INTO MembreVisualiseFichier (Fichier_ID, Membre_ID)
VALUES
(1, 2),
(2, 1);

INSERT INTO MembreRechercheFichier (Fichier_ID, Membre_ID)
VALUES
(1, 2),
(2, 1);

INSERT INTO MotsIndexFichier (MotCleID, Fichier_ID)
VALUES
(5, 1),
(5, 3),
(5, 5),
(5, 7),
(3, 9),
(3, 11),
(3, 13),
(3, 15),
(9, 17),
(9, 18),
(9, 19),
(9, 20);
