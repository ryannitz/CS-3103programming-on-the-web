DROP TABLE IF EXISTS PRESENTLIST;
CREATE TABLE PRESENTLIST (
    id                  INT             NOT NULL AUTO_INCREMENT,
    presentListName     varchar(100)    NOT NULL,
    presentListDesc     varchar(100)    NOT NULL,
    creationDate        BIGINT          NOT NULL,
    modificationDate    BIGINT          NOT NULL,
    userEmail          varchar(100)     NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(userEmail) references USER(userEmail)
);

