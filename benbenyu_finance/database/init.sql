-- ============================================================
-- 笨笨鱼财务系统 - MySQL 数据库初始化脚本
-- 数据库: benbenyu_finance
-- 字符集: utf8mb4
-- ============================================================

CREATE DATABASE IF NOT EXISTS benbenyu_finance
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE benbenyu_finance;

-- ------------------------------------------------------------
-- 用户表：支持个人用户(personal)与单位用户(organization)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id              INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username        VARCHAR(50)  NOT NULL UNIQUE COMMENT '登录用户名',
    password_hash   VARCHAR(255) NOT NULL COMMENT '密码哈希',
    role            ENUM('personal', 'organization') NOT NULL COMMENT '用户角色',
    display_name    VARCHAR(100) NOT NULL COMMENT '显示名称',
    org_name        VARCHAR(200) DEFAULT NULL COMMENT '单位名称(单位用户)',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_users_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统用户表';

-- ------------------------------------------------------------
-- 个人用户收支记录表
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS personal_records (
    id              INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    user_id         INT NOT NULL COMMENT '所属用户ID',
    record_date     DATE NOT NULL COMMENT '记账日期',
    record_type     ENUM('income', 'expense') NOT NULL COMMENT '类型:收入/支出',
    category        VARCHAR(50) NOT NULL COMMENT '分类(如餐饮、工资等)',
    amount          DECIMAL(12, 2) NOT NULL COMMENT '金额',
    payment_method  VARCHAR(30) DEFAULT '现金' COMMENT '支付方式',
    description     VARCHAR(500) DEFAULT NULL COMMENT '备注说明',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    CONSTRAINT fk_personal_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_personal_user_date (user_id, record_date),
    INDEX idx_personal_type (record_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='个人用户收支记录表';

-- ------------------------------------------------------------
-- 单位用户财政业务记录表（适配政府财务场景）
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS org_records (
    id                      INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    user_id                 INT NOT NULL COMMENT '所属用户ID',
    record_date             DATE NOT NULL COMMENT '业务日期',
    record_type             ENUM('income', 'expense') NOT NULL COMMENT '类型:收入/支出',
    voucher_no              VARCHAR(50) DEFAULT NULL COMMENT '凭证号',
    budget_code             VARCHAR(50) DEFAULT NULL COMMENT '预算科目编码',
    department              VARCHAR(100) DEFAULT NULL COMMENT '所属部门',
    project_name            VARCHAR(200) DEFAULT NULL COMMENT '项目名称',
    fund_source             VARCHAR(100) DEFAULT NULL COMMENT '资金来源',
    economic_classification VARCHAR(100) DEFAULT NULL COMMENT '经济分类',
    functional_classification VARCHAR(100) DEFAULT NULL COMMENT '功能分类',
    amount                  DECIMAL(14, 2) NOT NULL COMMENT '金额',
    payee_payer             VARCHAR(200) DEFAULT NULL COMMENT '收款方/付款方',
    handler                 VARCHAR(50) DEFAULT NULL COMMENT '经办人',
    approver                VARCHAR(50) DEFAULT NULL COMMENT '审批人',
    description             VARCHAR(500) DEFAULT NULL COMMENT '摘要说明',
    created_at              DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at              DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    CONSTRAINT fk_org_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_org_user_date (user_id, record_date),
    INDEX idx_org_voucher (voucher_no),
    INDEX idx_org_department (department)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='单位用户财政业务记录表';

-- 演示账号由后端启动时自动创建（seed.py）
-- 个人用户: personal / 123456
-- 单位用户: org / 123456
