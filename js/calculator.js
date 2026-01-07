// 실습: 계산기 만들기
// 1. 숫자 두 개 변수 할당
const a = 10;
const b = 5;

// 2. 산술 연산자 변수 할당
const operator = "+";   // +, -, *, /

// 3. 선택한 연산자에 따라서 계산 결과를 출력하는 프로그램 완성
// Hint: 조건문(if/else) 사용

if (operator === "+") {
    console.log(a + b);
} else if (operator === "-") {
    console.log(a - b);
} else if (operator === "*") {
    console.log(a * b);
} else if (operator === "/") {
    console.log(a / b);
} else {
    console.log("지원하지 않는 연산자입니다.")
}