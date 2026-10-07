/**
 * restructure-urls.js
 * Chuyển build/*.html (trừ index.html) → build/<name>/index.html
 * Đồng thời sửa tất cả href/src references từ relative → ../ prefix
 */

const fs   = require('fs');
const path = require('path');

const BUILD = path.join(__dirname, '..', 'build');

// Các trang cần chuyển thành thư mục (bỏ qua index.html)
const pages = [
  'about', 'browse', 'channel-analytics', 'channel-profile',
  'chat', 'contact', 'ecosystem', 'following', 'investors',
  'news', 'nlp-group', 'partners', 'playlist', 'sign-in',
  'sign-up', 'sitemap', 'trending', 'upload-videos',
  'video-live', 'video-normal', 'your-videos',
];

// Assets & links ở dạng relative cần thêm ../
// Pattern: href="xxx" hoặc src="xxx" với xxx KHÔNG bắt đầu bằng http/https/# hoặc ../
function addParentPrefix(html) {
  // css/js/img/font relative src & href
  html = html.replace(/(href|src)="(?!http|https|\/\/|#|data:|\.\.\/)(.*?)"/g, '$1="../$2"');
  // url() trong style attribute
  html = html.replace(/url\('(?!http|https|\/\/|data:|\.\.\/)([^']+)'\)/g, "url('../$1')");
  html = html.replace(/url\("(?!http|https|\/\/|data:|\.\.\/")([^"]+)"\)/g, 'url("../$1")');
  // background-image inline style
  html = html.replace(/(background-image:\s*url\()(?!http|https|\/\/|data:|\.\.\/)(['"]?)([^)'"]*)(['"]?)(\))/g,
    '$1$2../$3$4$5');
  return html;
}

// Sửa canonical & og:url: /about.html → /about/
function fixCanonical(html, name) {
  html = html.replace(
    new RegExp(`(nlpgroup\\.com\\.vn/)${name}\\.html`, 'g'),
    `$1${name}/`
  );
  return html;
}

// Sửa các link nội bộ *.html → ../*.html (trong thư mục con)
// vd href="about.html" → href="../about/" (hoặc ../about/index.html)
function fixInternalLinks(html) {
  // href="page.html" → href="../page/"
  html = html.replace(/href="(?!http|https|\/\/|#|\.\.\/)([a-z0-9-]+)\.html"/g, 'href="../$1/"');
  // href="../page.html" đã có ../ → href="../page/"
  html = html.replace(/href="\.\.\/([a-z0-9-]+)\.html"/g, 'href="../$1/"');
  return html;
}

let moved = 0;

pages.forEach(name => {
  const src  = path.join(BUILD, `${name}.html`);
  if (!fs.existsSync(src)) {
    console.warn(`  ⚠ Không tìm thấy: ${name}.html`);
    return;
  }

  const dir  = path.join(BUILD, name);
  const dest = path.join(dir, 'index.html');

  // Tạo thư mục
  fs.mkdirSync(dir, { recursive: true });

  // Đọc & xử lý nội dung
  let html = fs.readFileSync(src, 'utf8');
  html = addParentPrefix(html);
  html = fixCanonical(html, name);
  html = fixInternalLinks(html);

  // Ghi vào thư mục mới
  fs.writeFileSync(dest, html, 'utf8');

  // Xoá file cũ
  fs.unlinkSync(src);

  console.log(`  ✓ ${name}.html  →  ${name}/index.html`);
  moved++;
});

// Xử lý index.html riêng: chỉ sửa link nội bộ (không cần ../ prefix)
const indexPath = path.join(BUILD, 'index.html');
if (fs.existsSync(indexPath)) {
  let html = fs.readFileSync(indexPath, 'utf8');
  // href="about.html" → href="about/" (từ root, không cần ../)
  html = html.replace(/href="(?!http|https|\/\/|#|\.\.\/)([a-z0-9-]+)\.html"/g, 'href="$1/"');
  fs.writeFileSync(indexPath, html, 'utf8');
  console.log(`  ✓ index.html (internal links updated)`);
}

console.log(`\n✅ Hoàn tất: đã xử lý ${moved} trang + index.html`);
