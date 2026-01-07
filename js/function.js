function hello() {
    return "hello";
}

let 함수자체 = hello;
let 함수결과값 = hello();

console.log(함수자체);
console.log(함수결과값);