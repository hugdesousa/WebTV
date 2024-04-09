USE LDDPROJECT
IF EXISTS (
    SELECT
         *
    FROM
         SYS.TRIGGERS
    WHERE
         OBJECT_ID = OBJECT_ID(N'[dbo].[trg_AfterDeleteOnFichier]')
)

DROP TRIGGER [DBO].[TRG_AFTERDELETEONFICHIER];

GO

CREATE TRIGGER TRG_AFTERDELETEONFICHIER ON FICHIER AFTER
    DELETE AS
BEGIN
    DELETE FROM MEMBREVISUALISEFICHIER
    WHERE
        FICHIER_ID IN (
            SELECT
                FICHIER_ID
            FROM
                DELETED
        )
        DELETE FROM MEMBRERECHERCHEFICHIER
        WHERE
            FICHIER_ID IN (
                SELECT
                    FICHIER_ID
                FROM
                    DELETED
            )
            DELETE FROM INTERNAUTERECHERCHEFICHIER
            WHERE
                FICHIER_ID IN (
                    SELECT
                        FICHIER_ID
                    FROM
                        DELETED
                )
                DELETE FROM MOTSINDEXFICHIER
                WHERE
                    FICHIER_ID IN (
                        SELECT
                            FICHIER_ID
                        FROM
                            DELETED
                    ) END GO
 -- Procédure pour mettre à jour le profil d'un membre
                    CREATE PROCEDURE UPDATEMEMBERPROFILE @MEMBRE_ID INT,
                    @NOUVEAUPSEUDO VARCHAR(255),
                    @NOUVEAUEMAIL VARCHAR(255),
                    @NOUVEAUMOTDEPASSE VARCHAR(255),
                    @NOUVELLEIMAGEPROFIL VARCHAR(255) AS BEGIN UPDATE MEMBRE SET PSEUDO = @NOUVEAUPSEUDO,
                    EMAIL = @NOUVEAUEMAIL,
                    MOTDEPASSE = @NOUVEAUMOTDEPASSE,
                    IMAGEPROFIL = @NOUVELLEIMAGEPROFIL
                    WHERE
                        MEMBRE_ID = @MEMBRE_ID;
END;
GO ALTER TABLE MEMBRE ADD DERNIERECONNEXION DATETIME;
GO CREATE PROCEDURE MEMBERLOGIN @EMAIL VARCHAR(255), @MOTDEPASSE VARCHAR(255) AS
BEGIN
 -- Vérifier si les informations d'identification sont valides
    IF EXISTS (
        SELECT
            1
        FROM
            MEMBRE
        WHERE
            EMAIL = @EMAIL
            AND MOTDEPASSE = @MOTDEPASSE
    )
    BEGIN
 -- Mettre à jour les informations de connexion du membre
        UPDATE MEMBRE
        SET
            DERNIERECONNEXION = GETDATE(
            )
        WHERE
            EMAIL = @EMAIL;
 -- Retourner un statut de succès ou un message d'accueil, selon vos besoins
        SELECT
            'Connexion réussie' AS STATUS;
    END ELSE BEGIN
 -- Retourner un statut d'échec ou un message d'erreur, selon vos besoins
    SELECT 'Identifiants incorrects. Veuillez réessayer.' AS STATUS;
END
END;

GO