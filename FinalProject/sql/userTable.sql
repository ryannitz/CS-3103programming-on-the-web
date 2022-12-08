DROP TABLE IF EXISTS USER;
CREATE TABLE USER (
    id                  INT             NOT NULL AUTO_INCREMENT,
    userName            varchar(100)    NOT NULL,
    userEmail           varchar(100)    NOT NULL,
    creationDate        BIGINT          NOT NULL,
    modificationDate    BIGINT          NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT user_email_unique UNIQUE(userEmail)
);