-- 基金净值
CREATE TABLE IF NOT EXISTS `fund_nav`
(
    `code`          VARCHAR(10) NOT NULL COMMENT 'code',
    `name`          VARCHAR(100)  DEFAULT '' COMMENT '车款：2021款 55 TFSI quattro 首发先行特别版',
    `value_date`    VARCHAR(16)  NOT NULL COMMENT '净值日期',
    `unit_value`    DOUBLE(10, 5) DEFAULT 0 COMMENT '单位净值',
    `increase_rate` DOUBLE(10, 5) DEFAULT 0 COMMENT '涨幅',

    `create_ts`     TIMESTAMP     DEFAULT NOW(),
    `update_ts`     TIMESTAMP     DEFAULT NOW() ON UPDATE NOW(),

    PRIMARY KEY (`code`, `value_date`)

) ENGINE = InnoDB
  DEFAULT CHARSET = UTF8MB4
  COLLATE = utf8mb4_general_ci COMMENT '基金净值';
