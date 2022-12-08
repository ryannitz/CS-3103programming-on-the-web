DROP TABLE IF EXISTS PRESENT;
CREATE TABLE PRESENT (
    id                  INT             NOT NULL AUTO_INCREMENT,
    presentName         varchar(100)    NOT NULL,
    presentDesc         varchar(255)    NOT NULL,
    presentPrice        DOUBLE          SIGNED,
    creationDate        BIGINT          NOT NULL,
    modificationDate    BIGINT          NOT NULL,
    presentListId       INT             NOT NULL,
    userEmail           varchar(100)    NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(presentListId) references PRESENTLIST(id),
    FOREIGN KEY(userEmail) references PRESENTLIST(userEmail)
);

