drop database if exists BucketList;

CREATE DATABASE BucketList;

CREATE TABLE `BucketList`.`tbl_user` (
    `user_id` BIGINT UNIQUE AUTO_INCREMENT,
    `user_name` VARCHAR(45) NULL,
    `user_username` VARCHAR(45) NULL,
    `user_password` VARCHAR(255) NULL,
    PRIMARY KEY (`user_id`));

use BucketList;

drop procedure if exists `sp_createUser`;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(45),
    IN p_username VARCHAR(45),
    IN p_password VARCHAR(255)
)
BEGIN
    IF ( select exists (select 1 from tbl_user where (user_username = p_username or user_name = p_name)) ) THEN

        select 'Username Exists !!';

    ELSE

        insert into tbl_user
        (
            user_name,
            user_username,
            user_password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );

    END IF;
END$$
DELIMITER ;
drop procedure if exists `sp_validateLogin`;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
IN p_username VARCHAR(20)
)
BEGIN
    select * from tbl_user where (user_username = p_username or user_name = p_username);
END$$
DELIMITER ;