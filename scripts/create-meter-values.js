const mysql = require('mysql2/promise');
(async () => {
  const conn = await mysql.createConnection({
    host: 'lb-85416965-5de17699210eecee.elb.us-east-1.amazonaws.com',
    port: 9030, user: 'admin', password: 'Noname@2027',
    database: 'nlp_csms', connectTimeout: 15000
  });
  const sql = [
    "CREATE TABLE IF NOT EXISTS nlp_csms.meter_values (",
    "  id              BIGINT          NOT NULL,",
    "  ts              DATETIME        NOT NULL,",
    "  session_id      BIGINT          NOT NULL,",
    "  charge_point_id BIGINT          NOT NULL,",
    "  connector_idx   TINYINT         NOT NULL,",
    "  measurand       VARCHAR(50)     NOT NULL,",
    "  val             DECIMAL(14,4)   NOT NULL,",
    "  unit            VARCHAR(20)     NULL,",
    "  ctx             VARCHAR(30)     NULL",
    ")",
    "DUPLICATE KEY(id, ts)",
    "PARTITION BY RANGE(ts) (",
    "  PARTITION p2026q1 VALUES LESS THAN ('2026-04-01'),",
    "  PARTITION p2026q2 VALUES LESS THAN ('2026-07-01'),",
    "  PARTITION p2026q3 VALUES LESS THAN ('2026-10-01'),",
    "  PARTITION p2026q4 VALUES LESS THAN ('2027-01-01'),",
    "  PARTITION p2027q1 VALUES LESS THAN ('2027-04-01')",
    ")",
    "DISTRIBUTED BY HASH(id) BUCKETS 8",
    "PROPERTIES ('replication_num' = '1')"
  ].join('\n');

  try {
    await conn.query(sql);
    console.log('  ✓ meter_values created OK');
  } catch(e) {
    console.error('  FAIL:', e.message.split('\n')[0]);
  }

  const [t] = await conn.query('SHOW TABLES');
  console.log('\n📋 Tổng số bảng trong nlp_csms:', t.length);
  t.forEach(r => console.log('  ✓', Object.values(r)[0]));
  await conn.end();
})();
