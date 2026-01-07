// 실습: 합격 판정기

// 점수(score) 70 이상
// 출석률(attendance) 80 이상
// 과제 제출 여부(submitted) true
// 단, 점수가 90점 이상이면, 출석률 무시하고 합격

// 출력: "합격" 또는 "불합격"
// 힌트: &&, ||

let score = 80;
let attendance = 90;
let submitted = true;

if (
    // (score >= 70 && attendance >= 80 && submitted) || (score >= 90 && submitted)
    submitted && (
        (score >= 70 && attendance >= 80) || (score >= 90)
    )
) {
    console.log("합격");
} else {
    console.log("불합격");
}