const API_URL = "/api/tasks";

const taskForm = document.getElementById("taskForm");
const tasksContainer = document.getElementById("tasksContainer");

// Load all tasks
async function loadTasks() {
    try {
        const response = await fetch(API_URL);
        const tasks = await response.json();

        tasksContainer.innerHTML = "";

        if (tasks.length === 0) {
            tasksContainer.textContent = "No tasks available.";
            return;
        }

        tasks.forEach(task => {
            const taskItem = document.createElement("div");
            taskItem.className = "task-item";

            const title = document.createElement("h3");
            title.textContent = task.title;

            const description = document.createElement("p");
            description.textContent = task.description || "";

            const status = document.createElement("p");
            status.textContent = `Status: ${task.status}`;

            const updateButton = document.createElement("button");
            updateButton.textContent = "Mark Completed";
            updateButton.disabled = task.status === "Completed";
            updateButton.addEventListener("click", () => updateTask(task.id));

            const deleteButton = document.createElement("button");
            deleteButton.textContent = "Delete";
            deleteButton.className = "delete-btn";
            deleteButton.addEventListener("click", () => deleteTask(task.id));

            taskItem.append(title, description, status, updateButton, deleteButton);
            tasksContainer.appendChild(taskItem);
        });
    } catch (error) {
        tasksContainer.textContent = "Unable to load tasks.";
        console.error(error);
    }
}

// Add a new task
taskForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const title = document.getElementById("taskTitle").value.trim();
    const description = document.getElementById("taskDescription").value.trim();

    if (!title) return;

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, description })
        });

        if (!response.ok) throw new Error("Task creation failed");

        taskForm.reset();
        loadTasks();
    } catch (error) {
        alert("Unable to add task.");
        console.error(error);
    }
});

// Update task status
async function updateTask(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: "Completed" })
        });

        if (!response.ok) throw new Error("Task update failed");

        loadTasks();
    } catch (error) {
        alert("Unable to update task.");
        console.error(error);
    }
}

// Delete task
async function deleteTask(id) {
    if (!confirm("Are you sure you want to delete this task?")) return;

    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) throw new Error("Task deletion failed");

        loadTasks();
    } catch (error) {
        alert("Unable to delete task.");
        console.error(error);
    }
}

// Initial load
loadTasks();
