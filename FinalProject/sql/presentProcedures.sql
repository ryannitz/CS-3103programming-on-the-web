DELIMITER //
DROP PROCEDURE IF EXISTS createPresent //

CREATE PROCEDURE createPresent(IN presentName VARCHAR(100), IN presentDesc VARCHAR(100), 
                                IN presentPrice DOUBLE, IN presentListId INT, IN userEmail varchar(100))
BEGIN
  INSERT INTO PRESENT (presentName, presentDesc, presentPrice, creationDate, modificationDate, presentListId, userEmail)
  VALUES (presentName, presentDesc, presentPrice, CURDATE(), CURDATE(), presentListId, userEmail);

  SELECT LAST_INSERT_ID();
END //

DROP PROCEDURE IF EXISTS updatePresent //

CREATE PROCEDURE updatePresent(IN idIn INT, IN presentNameIn varchar(100), IN presentDescIn varchar(100), IN presentPriceIn DOUBLE, IN userEmailIn varchar(100))
BEGIN
  UPDATE PRESENT
  SET presentName = presentNameIn, presentDesc = presentDescIn, presentPrice = presentPriceIn, modificationDate = CURDATE()
  WHERE id = idIn;
END //

DROP PROCEDURE IF EXISTS deletePresent //

CREATE PROCEDURE deletePresent(IN presentId INT)
BEGIN
  DELETE FROM PRESENT WHERE id = presentId;
END //

DROP PROCEDURE IF EXISTS getPresentById //

CREATE PROCEDURE getPresentById(IN presentId INT)
BEGIN
  SELECT * from PRESENT WHERE id = presentId;
END //

DROP PROCEDURE IF EXISTS getPresentsByPresentList //

CREATE PROCEDURE getPresentsByPresentList(IN id INT)
BEGIN
  SELECT * from PRESENT WHERE presentListId = id;
END //


DROP PROCEDURE IF EXISTS getPresentsByUserEmail //

CREATE PROCEDURE getPresentsByUserEmail(IN userEmailIn INT)
BEGIN
  SELECT * from PRESENT WHERE userId = (SELECT id from USER where userEmail = userEmailIn);
END //

DELIMITER ;