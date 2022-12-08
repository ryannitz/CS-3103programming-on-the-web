DELIMITER //
DROP PROCEDURE IF EXISTS createPresentList //

CREATE PROCEDURE createPresentList(IN presentListName VARCHAR(100), IN presentListDesc VARCHAR(100), IN userEmail varchar(100))
BEGIN
  INSERT INTO PRESENTLIST (presentListName, presentListDesc, creationDate, modificationDate, userEmail)
  VALUES (presentListName, presentListDesc, CURDATE(), CURDATE(), userEmail);

  SELECT LAST_INSERT_ID();
END //

DROP PROCEDURE IF EXISTS updatePresentList //

CREATE PROCEDURE updatePresentList(IN presentListId INT, IN presentListNameIn VARCHAR(100), IN presentListDescIn VARCHAR(100), IN userEmailIn varchar(100))
BEGIN
  UPDATE PRESENTLIST 
  SET presentListName = presentListNameIn, presentListDesc = presentListDescIn, modificationDate = CURDATE() 
  WHERE id = presentListId AND userEmail = userEmailIn;

END //

DROP PROCEDURE IF EXISTS deletePresentList //

CREATE PROCEDURE deletePresentList(IN presentListId INT)
BEGIN
  DELETE FROM PRESENT WHERE presentListId = presentListId;
  DELETE FROM PRESENTLIST WHERE id = presentListId; 
END //

DROP PROCEDURE IF EXISTS getPresentListById //

CREATE PROCEDURE getPresentListById(IN PresentListId INT)
BEGIN
  SELECT * from PRESENTLIST WHERE id = PresentListId;
END //

DROP PROCEDURE IF EXISTS getPresentListByUserEmail //

CREATE PROCEDURE getPresentListByUserEmail(IN userEmailIn VARCHAR(100))
BEGIN
  SELECT * from PRESENTLIST WHERE userEmail = userEmailIn;
END //

DELIMITER ;