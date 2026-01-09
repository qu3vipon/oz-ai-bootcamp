const todoInput = document.querySelector("#todo-input");
const addBtn = document.querySelector("#add-btn");
const todoList = document.querySelector("#todo-list");

let todos = [];

addBtn.addEventListener("click", addTodo)

function addTodo() {
    const todo = todoInput.value.trim();
    todos.push(todo);  // todo 배열에 새로운 todo 추가
    todoInput.value = "";
    // localStorage에 저장
    renderTodos();
}

// todo 목록을 화면에 그리기
function renderTodos() {
    todoList.innerHTML = "";

    for (const [index, todo] of todos.entries()) {
        const li = document.createElement("li");
        li.className = "list-group-item d-flex justify-content-between align-items-center";
        li.textContent = todo;

        const deleteBtn = document.createElement("button");
        deleteBtn.className = "btn btn-sm btn-danger";
        deleteBtn.textContent = "삭제";
        deleteBtn.addEventListener("click", () => deleteTodo(index));

        li.appendChild(deleteBtn);
        todoList.appendChild(li);
    }
}

function deleteTodo(index) {
    todos.splice(index, 1);
    renderTodos();
}