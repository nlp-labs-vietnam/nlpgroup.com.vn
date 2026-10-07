const mysql = require('mysql2/promise');
const fs = require('fs');
const path = require('path');

const baseConfig = {
  host: 'lb-85416965-5de17699210eecee.elb.us-east-1.amazonaws.com',
  port: 9030,
  user: 'admin',
  password: 'Noname@2027',
  connectTimeout: 15000,
};

async function runStatements(conn, statements) {
  let ok = 0, skip = 0, fail = 0;
  for (const stmt of statements) {
    const trimmed = stmt.trim();
    if (!trimmed || trimmed.startsWith('--')) continue;
    try {
      await conn.query(trimmed);
      const preview = trimmed.replace(/\s+/g, ' ').substring(0, 80);
      console.log(`  ✓ ${preview}`);
      ok++;
    } catch (err) {
      if (
        err.message.includes('already exists') ||
        err.message.includes('Duplicate entry') ||
        err.message.includes('Table already exists')
      ) {
        skip++;
      } else {
        console.warn(`  ⚠ FAIL: ${err.message.split('\n')[0]}`);
        console.warn(`    → ${trimmed.substring(0, 80)}`);
        fail++;
      }
    }
  }
  return { ok, skip, fail };
}

(async () => {
  let conn;
  try {
    // Step 1: tạo database (không cần chỉ định DB)
    conn = await mysql.createConnection(baseConfig);
    console.log('✅ Kết nối thành công!\n');
    console.log('▶ Tạo database nlp_csms...');
    await conn.query('CREATE DATABASE IF NOT EXISTS nlp_csms');
    console.log('  ✓ Database nlp_csms sẵn sàng\n');
    await conn.end();

    // Step 2: kết nối lại vào nlp_csms
    conn = await mysql.createConnection({ ...baseConfig, database: 'nlp_csms' });
    console.log('▶ Đang chạy schema...\n');

    const sqlFile = path.join(__dirname, 'schema.sql');
    const sql = fs.readFileSync(sqlFile, 'utf8');

    // Bỏ qua statement CREATE DATABASE (đã chạy rồi)
    // Loại bỏ comment lines trước khi split
    const cleanSql = sql
      .split('\n')
      .filter(line => !line.trim().startsWith('--'))
      .join('\n');

    const statements = cleanSql
      .split(/;\s*\n/)
      .map(s => s.trim())
      .filter(s => s.length > 0 && !s.toUpperCase().startsWith('CREATE DATABASE'));

    const { ok, skip, fail } = await runStatements(conn, statements);
    console.log(`\n📊 Kết quả: ${ok} OK | ${skip} bỏ qua | ${fail} lỗi`);

    // Step 3: verify
    const [tables] = await conn.query('SHOW TABLES');
    console.log('\n📋 Bảng trong nlp_csms:');
    tables.forEach(r => console.log('  ✓', Object.values(r)[0]));

  } catch (err) {
    console.error('❌ Lỗi:', err.message);
    process.exit(1);
  } finally {
    if (conn) await conn.end();
  }
})();
