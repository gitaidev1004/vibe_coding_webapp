// 파일 저장/열기와 관련된 함수를 모아 둔 모듈

export function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

// 일반 텍스트(.txt)를 편집기에 넣을 HTML로 변환한다.
export function textToHtml(text) {
  return text
    .split(/\r?\n/)
    .map((line) => "<div>" + (escapeHtml(line) || "<br>") + "</div>")
    .join("");
}

// 열어 온 HTML에서 스크립트와 이벤트 속성을 제거한다.
export function sanitizeHtml(html) {
  const doc = new DOMParser().parseFromString(html, "text/html");
  doc.querySelectorAll("script, iframe, object, embed").forEach((el) => el.remove());
  doc.body.querySelectorAll("*").forEach((el) => {
    Array.from(el.attributes).forEach((attr) => {
      if (attr.name.toLowerCase().startsWith("on")) {
        el.removeAttribute(attr.name);
      }
    });
  });
  return doc.body.innerHTML;
}

function readFileAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result));
    reader.onerror = () => reject(reader.error);
    reader.readAsText(file, "utf-8");
  });
}

// 선택한 파일을 읽어 편집기에 넣을 HTML 문자열을 돌려준다.
export async function openDocument(file) {
  const text = await readFileAsText(file);
  if (/\.html?$/i.test(file.name)) {
    return sanitizeHtml(text);
  }
  return textToHtml(text);
}

// 편집기 내용을 .html 파일로 내려받는다.
export function saveHtmlFile(fileName, bodyHtml) {
  const name = /\.html?$/i.test(fileName) ? fileName : fileName + ".html";
  const content =
    '<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="UTF-8">\n' +
    "<title>" + escapeHtml(name) + "</title>\n</head>\n<body>\n" +
    bodyHtml + "\n</body>\n</html>\n";
  const blob = new Blob([content], { type: "text/html;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = name;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}
