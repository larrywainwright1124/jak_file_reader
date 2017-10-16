DROP PROCEDURE IF EXISTS adjustment;
DELIMITER //
CREATE PROCEDURE adjustment(p_xid          INT, p_amt DECIMAL(10, 2), p_source_id INT,
                            p_source_table VARCHAR(45), OUT p_resp_code VARCHAR(2))
  BEGIN
    DECLARE v_otb DECIMAL(10, 2);
    DECLARE v_bal_id INT;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
      ROLLBACK;
      SET p_resp_code = '01';
      SET AUTOCOMMIT = 1;
    END;

    SET p_resp_code = '00';
    SET AUTOCOMMIT = 0;

    SELECT
      b.bal_id,
      b.open_to_buy
    INTO v_bal_id, v_otb
    FROM ac_account ac
      JOIN ac_balance b ON b.bal_id = ac.bal_id
    WHERE ac.xid = p_xid;


    IF v_otb - p_amt > 0
    THEN
      START TRANSACTION;

      UPDATE ac_balance
      SET open_to_buy = open_to_buy - p_amt
      WHERE bal_id = v_bal_id;

      INSERT INTO activity (
        act_type, amount, in_ts, source_id, source_table
      ) VALUES (
        'ADJ', p_amt, SYSDATE(), p_source_id, p_source_table
      );
      COMMIT;

    ELSE
      SET p_resp_code = '02';
    END IF;
    SET AUTOCOMMIT = 1;
  END //
DELIMITER ;