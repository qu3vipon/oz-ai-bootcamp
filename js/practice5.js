// 점수 배열을 받아서, 평균을 반환하는 함수
function getAverage(scores) {
    if (scores.length === 0) {
        throw new Error("빈 배열입니다");
    }

    let sum = 0;
    for (const score of scores) {
        sum += score;
    }
    return sum / scores.length;
}

let result = getAverage([]);
console.log(result);
