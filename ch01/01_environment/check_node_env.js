/**
 * ch01/01_environment/check_node_env.js
 * Node.js / Vue.js 3 / Vite 개발 환경 확인 스크립트
 */
const { execSync } = require("child_process");

function run(cmd) {
  try {
    return execSync(cmd, { encoding: "utf-8" }).trim();
  } catch (err) {
    return null;
  }
}

console.log("=== Node.js 개발 환경 점검 ===");
console.log(`Node.js 버전 : ${process.version}`);

const npmVersion = run("npm --version");
console.log(`npm 버전     : ${npmVersion !== null ? npmVersion : "확인 불가"}`);

const major = parseInt(process.version.replace("v", "").split(".")[0], 10);
if (major >= 18) {
  console.log(" -> Vue.js 3 / Vite 실습에 적합한 버전입니다.");
} else {
  console.log(" -> Node.js 18 이상 버전 사용을 권장합니다.");
}

console.log();
console.log("=== Vite 프로젝트 생성 명령 안내 ===");
console.log("npm create vite@latest my-app -- --template vue");
