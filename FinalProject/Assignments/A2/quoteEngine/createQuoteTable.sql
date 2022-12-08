DROP TABLE IF EXISTS quotes;
CREATE TABLE quotes (
  quoteId   INT           NOT NULL AUTO_INCREMENT,
  quoteVal  varchar(255)  NOT NULL,
  PRIMARY KEY (quoteId)
);
