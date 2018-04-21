DROP PROCEDURE IF EXISTS ROLE_MENU;

DELIMITER $$

CREATE PROCEDURE ROLE_MENU(IN RM_NAME VARCHAR(50),IN RM_CODE VARCHAR(20), IN VID VARCHAR(9))
BEGIN

DECLARE ID_NEW VARCHAR(99);
DECLARE NAME_NEW VARCHAR(50);
DECLARE KEY_NEW VARCHAR(50);
DECLARE MENU_NEW VARCHAR(50);
DECLARE ROLE_NEW VARCHAR(30);
DECLARE ACTIVE_NEW BOOLEAN;
DECLARE ACCESS_MENU_NAME VARCHAR(50);
DECLARE MENU_COUNT INT(99);
DECLARE VID_NEW VARCHAR(50);

DECLARE V_FINISHED INTEGER DEFAULT 0;
DECLARE V_CODE VARCHAR(99);

DECLARE ROLE_MENU_CUR CURSOR FOR (SELECT name FROM access_data WHERE code = (CASE RM_CODE WHEN 'MENU' THEN 'ROLE' ELSE 'MENU' END )) ;

DECLARE CONTINUE HANDLER FOR NOT FOUND SET V_FINISHED = 1;
SET V_CODE = (CASE RM_CODE WHEN 'MENU' THEN 'ROLE' ELSE 'MENU' END );

INSERT INTO access_log_data ( data ) VALUES( CONCAT('PASS_CODE: ', RM_CODE ));
INSERT INTO access_log_data  ( data ) VALUES( CONCAT('ACCESS_DATA_CODE: ', V_CODE) );
INSERT INTO access_log_data  ( data ) VALUES( CONCAT('COUNT OF DATA: ', (SELECT COUNT(1) FROM access_data WHERE code= V_CODE )) );

OPEN ROLE_MENU_CUR;

    IF RM_CODE = 'MENU' THEN
        I_LOOP:LOOP
            FETCH ROLE_MENU_CUR INTO ACCESS_MENU_NAME;
                IF V_FINISHED = 1 THEN
                    LEAVE  I_LOOP;
                END IF;
                SET NAME_NEW =  RM_NAME;
                SET MENU_NEW = LOWER( REPLACE(NAME_NEW, ' ','_' ) );
                SET ROLE_NEW = UPPER( REPLACE(ACCESS_MENU_NAME, ' ','_' )) ;
                SET VID_NEW = UPPER( REPLACE(VID, ' ','_' ));
                SET ID_NEW = CONCAT( VID_NEW,'_',UPPER(ROLE_NEW), '_', UPPER(MENU_NEW) );
                IF ROLE_NEW = 'SUPER_ADMIN' THEN
                    SET ACTIVE_NEW = TRUE;
                ELSE
                    SET ACTIVE_NEW = FALSE;
                END IF;
                SELECT COUNT(1) INTO MENU_COUNT FROM access_menu WHERE id=ID_NEW;
                IF MENU_COUNT = 0 THEN
                    INSERT INTO access_log_data  ( data ) VALUES( CONCAT( "INSERT INTO access_menu(id, name, menu, role, active, vid) VALUES (", "'", ID_NEW, "','", NAME_NEW, "','", MENU_NEW ,"','", ROLE_NEW, "','", ACTIVE_NEW, "','", VID, "'", ");") );
                    INSERT INTO access_menu(id, name, menu, role, active, vid) VALUES (ID_NEW, NAME_NEW, MENU_NEW, ROLE_NEW, ACTIVE_NEW, VID);
                END IF;
            END LOOP I_LOOP;
        END IF;

        IF RM_CODE='ROLE' THEN
            I_LOOP:LOOP
                FETCH ROLE_MENU_CUR INTO ACCESS_MENU_NAME;
                    IF V_FINISHED = 1 THEN
                        LEAVE  I_LOOP;
                    END IF;
                    SET MENU_NEW = LOWER(REPLACE(ACCESS_MENU_NAME, ' ','_' ));
                    SET NAME_NEW =  ACCESS_MENU_NAME;
                    SET ROLE_NEW = UPPER(REPLACE(RM_NAME, ' ', '_' ));
                    SET VID_NEW=UPPER(REPLACE(VID, ' ','_' ));
                    SET ID_NEW = CONCAT(VID_NEW,'_',UPPER(ROLE_NEW), '_', UPPER(MENU_NEW));
                    IF ROLE_NEW = 'SUPER_ADMIN' THEN
                        SET ACTIVE_NEW = TRUE;
                    ELSE
                        SET ACTIVE_NEW = FALSE;
                    END IF;
                    SELECT COUNT(1) INTO MENU_COUNT FROM access_menu WHERE id=ID_NEW;
                    IF MENU_COUNT = 0 THEN
                        INSERT INTO access_log_data  ( data ) VALUES( CONCAT( "INSERT INTO access_menu(id, name, menu, role, active, vid) VALUES (", "'", ID_NEW, "','", NAME_NEW, "','", MENU_NEW ,"','", ROLE_NEW, "','", ACTIVE_NEW, "','", VID, "'", ");") );
                        INSERT INTO access_menu(id, name, menu, role, active, vid) VALUES (ID_NEW, NAME_NEW, MENU_NEW, ROLE_NEW, ACTIVE_NEW, VID);
                    END IF;
                END LOOP I_LOOP;
        END IF;
        SELECT COUNT(1) INTO MENU_COUNT FROM access_data WHERE name=RM_NAME AND code=RM_CODE;
        IF MENU_COUNT = 0 THEN
            INSERT INTO access_data(name, code, val) VALUES (RM_NAME, RM_CODE, UPPER(REPLACE(RM_NAME, ' ', '_' )) );
        END IF;
        INSERT INTO access_log_data  ( data ) VALUES ('DONE');
CLOSE ROLE_MENU_CUR;
END$$

DELIMITER ;

CALL ROLE_MENU ('Super Admin', 'ROLE', 'DFF');
CALL ROLE_MENU ('Anonymous', 'ROLE', 'DFF');
CALL ROLE_MENU ('User', 'ROLE', 'DFF');
CALL ROLE_MENU ('Admin', 'ROLE', 'DFF');

CALL ROLE_MENU ('Consumer', 'MENU', 'DFF');


