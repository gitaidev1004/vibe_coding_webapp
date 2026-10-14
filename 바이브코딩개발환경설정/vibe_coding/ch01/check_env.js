// 실습 환경 점검 스크립트: Node.js 버전과 운영체제를 확인한다.
const [major] = process.versions.node.split(".").map(Number);

console.log("Node.js 버전:", process.version);
console.log("운영체제:", process.platform);

if (major < 18) {
  console.log("결과: Node.js 18 이상으로 업데이트해야 합니다.");
  process.exitCode = 1;
} else {
  console.log("결과: 실습 환경을 사용할 수 있습니다.");
}
