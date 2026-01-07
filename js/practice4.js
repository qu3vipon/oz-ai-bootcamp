// 함수 선언
function checkPass(score, submitted) {
    if (submitted) {
        if (score >= 90) {
            return "최우수";
        } else if (score >= 80) {
            return "우수";
        } else {
            return "합격";
        }
    }
    return "불합격";
}

let output = checkPass(70, true);
console.log(output);
