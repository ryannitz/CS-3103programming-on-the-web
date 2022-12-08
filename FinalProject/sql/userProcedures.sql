DELIMITER //
DROP PROCEDURE IF EXISTS createUsers //

CREATE PROCEDURE createUsers(IN userName VARCHAR(100), IN userEmail VARCHAR(100))
BEGIN
  INSERT INTO USER (userName, userEmail, creationDate, modificationDate)
  VALUES (userName, userEmail, CURDATE(), CURDATE());
END //

DROP PROCEDURE IF EXISTS updateUser //

CREATE PROCEDURE updateUser(IN userNameIn VARCHAR(100), IN userEmailIn VARCHAR(100))
BEGIN
  UPDATE USER 
  SET userName = userNameIn, modificationDate = CURDATE() 
  WHERE userEmail = userEmailIn;
END //

DROP PROCEDURE IF EXISTS deleteUser //

CREATE PROCEDURE deleteUser(IN userEmailIn VARCHAR(100))
BEGIN
  DELETE FROM PRESENT WHERE userEmail = userEmailIn;
  DELETE FROM PRESENTLIST WHERE userEmail = userEmailIn;
  DELETE FROM USER WHERE userEmail = userEmailIn;
END //

DROP PROCEDURE IF EXISTS getUserById //

CREATE PROCEDURE getUserById(IN userId INT)
BEGIN
  SELECT * from USER WHERE id = userId;
END //

DROP PROCEDURE IF EXISTS getUserByEmail //

CREATE PROCEDURE getUserByEmail(IN userEmailIn VARCHAR(100))
BEGIN
  SELECT * from USER WHERE userEmail = userEmailIn;
END //

DROP PROCEDURE IF EXISTS getUsers //

CREATE PROCEDURE getUsers()
BEGIN
  SELECT * from USER;
END //

DELIMITER ;