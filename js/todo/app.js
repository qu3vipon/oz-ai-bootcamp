/* =====================
    To-Do Logic
===================== */
const todoInput = document.querySelector("#todo-input");
const addBtn = document.querySelector("#add-btn");
const todoList = document.querySelector("#todo-list");

let todos = [];

// 복원
const savedTodos = JSON.parse(localStorage.getItem("todos"));

if (savedTodos) {
    todos = savedTodos;
    renderTodos();
}

function addTodo() {
    const text = todoInput.value.trim();
    if (text === "") {
        alert("할 일을 입력하세요");
        return;
    }

    todos.push(text);
    todoInput.value = "";
    saveTodos();
    renderTodos();
}

function deleteTodo(index) {
    todos.splice(index, 1);
    saveTodos();
    renderTodos();
}

function renderTodos() {
    todoList.innerHTML = "";

    todos.forEach((todo, index) => {
        const li = document.createElement("li");
        li.className =
        "list-group-item d-flex justify-content-between align-items-center";
        li.textContent = todo;

        const btn = document.createElement("button");
        btn.className = "btn btn-sm btn-danger";
        btn.textContent = "삭제";
        btn.addEventListener("click", () => deleteTodo(index));

        li.appendChild(btn);
        todoList.appendChild(li);
    });
}

function saveTodos() {
    localStorage.setItem("todos", JSON.stringify(todos));
}

addBtn.addEventListener("click", addTodo);
    todoInput.addEventListener("keydown", e => {
    if (e.key === "Enter") addTodo();
});

/* =====================
    Pomodoro Timer Logic
===================== */
const timeInput = document.querySelector("#time-input");
const startBtn = document.querySelector("#start-timer");
const stopBtn = document.querySelector("#stop-timer");
const display = document.querySelector("#timer-display");

let timerId = null;
let remainingTime = 0;

function updateDisplay() {
    const min = Math.floor(remainingTime / 60);
    const sec = remainingTime % 60;

    display.className = "fs-3";
    display.textContent =
        String(min).padStart(2, "0") + ":" +
        String(sec).padStart(2, "0");
}

startBtn.addEventListener("click", function () {
    if (timerId !== null) return;

    const minutes = Number(timeInput.value);
    if (minutes <= 0) {
        alert("시간을 입력하세요");
        return;
    }

    remainingTime = minutes * 60;
    updateDisplay();

    timerId = setInterval(function () {
        remainingTime--;

        if (remainingTime <= 0) {
            clearInterval(timerId);
            timerId = null;
            display.className = "fs-6 text-muted";
            display.textContent = "시간을 설정하세요.";
            alert("Pomodoro 종료!");
        } else {
            updateDisplay();
        }
    }, 1000);
});

stopBtn.addEventListener("click", function () {
    clearInterval(timerId);
    timerId = null;
});