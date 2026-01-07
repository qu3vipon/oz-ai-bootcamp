let numbers = [10, 20, 30, "one", "two"];

// console.log(numbers[0]);
// console.log(numbers[3]);

// numbers.length만 순회
// for (let i = 0; i < numbers.length; i++) {
//     console.log(numbers[i]);
// }


// for...of
// for (const num of numbers) {
//     if (num === 30) {
//         break
//     }
//     console.log(num);
// }


// forEach
// numbers.forEach(score => {
//     console.log(score);
// })


for (const [i, num] of numbers.entries()) {
    console.log(i, num);
}