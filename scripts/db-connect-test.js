const mysql = require('mysql2/promise');

const config = {
  host: 'lb-85416965-5de17699210eecee.elb.us-east-1.amazonaws.com',
  port: 9030,
  user: 'admin',
  password: 'Noname@2027',
  connectTimeout: 15000,
};

(async () => {
  let conn;
  try {
    conn = await mysql.createConnection(config);
    console.log('✅ Kết nối thành công!');
    const [rows] = await conn.query('SHOW DATABASES');
    console.log('Databases hiện có:');
    rows.forEach(r => console.log(' -', Object.values(r)[0]));
  } catch (err) {
    console.error('❌ Lỗi kết nối:', err.message);
  } finally {
    if (conn) await conn.end();
  }
})();
