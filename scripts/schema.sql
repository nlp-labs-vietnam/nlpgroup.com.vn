-- ============================================================
-- NLP GROUP — CSMS (Charge Station Management System)
-- Apache Doris compatible schema
-- Created: 2026
-- ============================================================

CREATE DATABASE IF NOT EXISTS nlp_csms;

-- ============================================================
-- TABLE: operators
-- ============================================================
CREATE TABLE IF NOT EXISTS nlp_csms.operators (
    id              BIGINT          NOT NULL,
    code            VARCHAR(32)     NOT NULL,
    name            VARCHAR(200)    NOT NULL,
    tax_code        VARCHAR(20)     NULL,
    address         VARCHAR(500)    NULL,
    phone           VARCHAR(20)     NULL,
    email           VARCHAR(100)    NULL,
    bank_name       VARCHAR(100)    NULL,
    bank_branch     VARCHAR(100)    NULL,
    bank_account    VARCHAR(50)     NULL,
    is_active       TINYINT         NOT NULL DEFAULT 1,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
)
DUPLICATE KEY(id)
DISTRIBUTED BY HASH(id) BUCKETS 4
PROPERTIES ("replication_num" = "1");

-- ============================================================
-- TABLE: stations
-- ============================================================
CREATE TABLE IF NOT EXISTS nlp_csms.stations (
    id              BIGINT          NOT NULL,
    operator_id     BIGINT          NOT NULL,
    code            VARCHAR(50)     NOT NULL,
    name            VARCHAR(200)    NOT NULL,
    address         VARCHAR(500)    NULL,
    lat             DECIMAL(10,7)   NULL,
    lng             DECIMAL(10,7)   NULL,
    province        VARCHAR(100)    NULL,
    district        VARCHAR(100)    NULL,
    is_active       TINYINT         NOT NULL DEFAULT 1,
    ocpp_version    VARCHAR(10)     NULL,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
)
DUPLICATE KEY(id)
DISTRIBUTED BY HASH(id) BUCKETS 4
PROPERTIES ("replication_num" = "1");

-- ============================================================
-- TABLE: charge_points
-- ============================================================
CREATE TABLE IF NOT EXISTS nlp_csms.charge_points (
    id                  BIGINT          NOT NULL,
    station_id          BIGINT          NOT NULL,
    cp_id               VARCHAR(50)     NOT NULL,
    model               VARCHAR(100)    NULL,
    vendor              VARCHAR(100)    NULL,
    serial_number       VARCHAR(100)    NULL,
    firmware_version    VARCHAR(50)     NULL,
    max_power_kw        DECIMAL(6,2)    NULL,
    connector_count     TINYINT         NOT NULL DEFAULT 2,
    cp_status           VARCHAR(20)     NOT NULL DEFAULT 'Available',
    last_heartbeat      DATETIME        NULL,
    created_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
)
DUPLICATE KEY(id)
DISTRIBUTED BY HASH(id) BUCKETS 4
PROPERTIES ("replication_num" = "1");

-- ============================================================
-- TABLE: connectors
-- ============================================================
CREATE TABLE IF NOT EXISTS nlp_csms.connectors (
    id                  BIGINT          NOT NULL,
    charge_point_id     BIGINT          NOT NULL,
    connector_idx       TINYINT         NOT NULL,
    connector_type      VARCHAR(20)     NULL,
    max_power_kw        DECIMAL(6,2)    NULL,
    conn_status         VARCHAR(20)     NOT NULL DEFAULT 'Available',
    created_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
)
DUPLICATE KEY(id)
DISTRIBUTED BY HASH(id) BUCKETS 4
PROPERTIES ("replication_num" = "1");

-- ============================================================
-- TABLE: users
-- ============================================================
CREATE TABLE IF NOT EXISTS nlp_csms.users (
    id              BIGINT          NOT NULL,
    uid             VARCHAR(64)     NOT NULL,
    phone           VARCHAR(20)     NULL,
    email           VARCHAR(100)    NULL,
    full_name       VARCHAR(200)    NULL,
    avatar_url      VARCHAR(500)    NULL,
    id_token        VARCHAR(100)    NULL,
    wallet_balance  DECIMAL(15,2)   NOT NULL DEFAULT 0,
    is_active       TINYINT         NOT NULL DEFAULT 1,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
)
DUPLICATE KEY(id)
DISTRIBUTED BY HASH(id) BUCKETS 4
PROPERTIES ("replication_num" = "1");

-- ============================================================
-- TABLE: tariffs
-- ============================================================
CREATE TABLE IF NOT EXISTS nlp_csms.tariffs (
    id              BIGINT          NOT NULL,
    operator_id     BIGINT          NOT NULL,
    name            VARCHAR(100)    NOT NULL,
    price_per_kwh   DECIMAL(10,2)   NOT NULL,
    peak_price      DECIMAL(10,2)   NULL,
    off_peak_price  DECIMAL(10,2)   NULL,
    peak_start      VARCHAR(8)      NULL,
    peak_end        VARCHAR(8)      NULL,
    currency        VARCHAR(5)      NOT NULL DEFAULT 'VND',
    is_active       TINYINT         NOT NULL DEFAULT 1,
    effective_from  DATE            NULL,
    effective_to    DATE            NULL,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
)
DUPLICATE KEY(id)
DISTRIBUTED BY HASH(id) BUCKETS 4
PROPERTIES ("replication_num" = "1");

-- ============================================================
-- TABLE: charging_sessions
-- ============================================================
CREATE TABLE IF NOT EXISTS nlp_csms.charging_sessions (
    id                  BIGINT          NOT NULL,
    transaction_id      VARCHAR(64)     NOT NULL,
    charge_point_id     BIGINT          NOT NULL,
    connector_idx       TINYINT         NOT NULL,
    user_id             BIGINT          NULL,
    id_tag              VARCHAR(50)     NULL,
    tariff_id           BIGINT          NULL,
    start_time          DATETIME        NOT NULL,
    stop_time           DATETIME        NULL,
    start_meter_wh      BIGINT          NOT NULL DEFAULT 0,
    stop_meter_wh       BIGINT          NULL,
    energy_kwh          DECIMAL(10,3)   NULL,
    duration_sec        INT             NULL,
    soc_start           TINYINT         NULL,
    soc_end             TINYINT         NULL,
    amount              DECIMAL(15,2)   NULL,
    session_status      VARCHAR(20)     NOT NULL DEFAULT 'Active',
    stop_reason         VARCHAR(50)     NULL,
    created_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
)
DUPLICATE KEY(id)
DISTRIBUTED BY HASH(id) BUCKETS 8
PROPERTIES ("replication_num" = "1");

-- ============================================================
-- TABLE: meter_values  (time-series)
-- ============================================================
CREATE TABLE IF NOT EXISTS nlp_csms.meter_values (
    id              BIGINT          NOT NULL,
    ts              DATETIME        NOT NULL,
    session_id      BIGINT          NOT NULL,
    charge_point_id BIGINT          NOT NULL,
    connector_idx   TINYINT         NOT NULL,
    measurand       VARCHAR(50)     NOT NULL,
    val             DECIMAL(14,4)   NOT NULL,
    unit            VARCHAR(20)     NULL,
    ctx             VARCHAR(30)     NULL
)
DUPLICATE KEY(id, ts)
PARTITION BY RANGE(ts) (
    PARTITION p2026q1 VALUES LESS THAN ("2026-04-01"),
    PARTITION p2026q2 VALUES LESS THAN ("2026-07-01"),
    PARTITION p2026q3 VALUES LESS THAN ("2026-10-01"),
    PARTITION p2026q4 VALUES LESS THAN ("2027-01-01"),
    PARTITION p2027q1 VALUES LESS THAN ("2027-04-01")
)
DISTRIBUTED BY HASH(id) BUCKETS 8
PROPERTIES ("replication_num" = "1");

-- ============================================================
-- TABLE: ocpp_commands
-- ============================================================
CREATE TABLE IF NOT EXISTS nlp_csms.ocpp_commands (
    id              BIGINT          NOT NULL,
    charge_point_id BIGINT          NOT NULL,
    connector_idx   TINYINT         NULL,
    command         VARCHAR(50)     NOT NULL,
    payload         TEXT            NULL,
    response        TEXT            NULL,
    cmd_status      VARCHAR(20)     NOT NULL DEFAULT 'Pending',
    issued_by       VARCHAR(100)    NULL,
    issued_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    responded_at    DATETIME        NULL
)
DUPLICATE KEY(id)
DISTRIBUTED BY HASH(id) BUCKETS 4
PROPERTIES ("replication_num" = "1");

-- ============================================================
-- TABLE: wallet_transactions
-- ============================================================
CREATE TABLE IF NOT EXISTS nlp_csms.wallet_transactions (
    id              BIGINT          NOT NULL,
    user_id         BIGINT          NOT NULL,
    session_id      BIGINT          NULL,
    tx_type         VARCHAR(20)     NOT NULL,
    amount          DECIMAL(15,2)   NOT NULL,
    balance_before  DECIMAL(15,2)   NOT NULL,
    balance_after   DECIMAL(15,2)   NOT NULL,
    payment_method  VARCHAR(30)     NULL,
    payment_ref     VARCHAR(100)    NULL,
    note            VARCHAR(300)    NULL,
    tx_status       VARCHAR(20)     NOT NULL DEFAULT 'Success',
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
)
DUPLICATE KEY(id)
DISTRIBUTED BY HASH(id) BUCKETS 4
PROPERTIES ("replication_num" = "1");

-- ============================================================
-- TABLE: admin_users
-- ============================================================
CREATE TABLE IF NOT EXISTS nlp_csms.admin_users (
    id              BIGINT          NOT NULL,
    operator_id     BIGINT          NOT NULL,
    username        VARCHAR(100)    NOT NULL,
    email           VARCHAR(100)    NULL,
    password_hash   VARCHAR(255)    NOT NULL,
    user_role       VARCHAR(30)     NOT NULL DEFAULT 'noc',
    is_active       TINYINT         NOT NULL DEFAULT 1,
    last_login      DATETIME        NULL,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
)
DUPLICATE KEY(id)
DISTRIBUTED BY HASH(id) BUCKETS 4
PROPERTIES ("replication_num" = "1");
