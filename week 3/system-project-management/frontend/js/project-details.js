// User role check and navbar setup
requireAuth();
const currentRole = localStorage.getItem("user_role");
fillNavbarUser();
document.getElementById("logoutBtn").addEventListener("click", logout);

// --- Globals ---
const params = new URLSearchParams(window.location.search);
const projectId = params.get("id");
if (!projectId) {
    window.location.href = "projects.html";
}
const usersMap = {};

// --- DOM Elements ---
const taskForm = document.getElementById("taskForm");
const taskIdField = document.getElementById("taskId");
const tasksGrid = document.getElementById("tasksGrid");
const cancelBtn = document.getElementById("cancelBtn");
const formTitle = document.getElementById("formTitle");
const formErrorMessage = document.getElementById("formErrorMessage");
const projectInfoCard = document.getElementById("projectInfoCard");

// --- Helper Functions ---
function showError(element, message) {
    element.innerHTML = `<div class="card error-message">${message}</div>`;
}
function showFormError(message) {
    formErrorMessage.textContent = message;
    formErrorMessage.style.display = "block";
}
function clearFormError() {
    formErrorMessage.textContent = "";
    formErrorMessage.style.display = "none";
}

// Validation functions
function validateTaskTitle(title) {
    return title.trim().length >= 1 && title.trim().length <= 200;
}

function validateTaskDescription(description) {
    return description.trim().length <= 1000; // Optional but limited
}

function getStatusBadge(status) {
    const statusMap = { completed: "badge-success", active: "badge-info", in_progress: "badge-info", planned: "badge-warning", todo: "badge-warning" };
    return statusMap[status] || "badge-gray";
}

function getPriorityBadge(priority) {
    const priorityMap = { high: "badge-danger", medium: "badge-warning", low: "badge-info" };
    return priorityMap[priority] || "badge-gray";
}

function formatDate(dateString) {
    if (!dateString) return "N/A";
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function formatDateForInput(dateString) {
    if (!dateString) return "";
    return dateString.split('T')[0];
}

// --- UI Toggling and Form Handling ---
function resetAndHideForm() {
    clearFormError();
    formTitle.textContent = "Create Task";
    taskForm.reset();
    taskIdField.value = "";
    cancelBtn.style.display = "none";
}

cancelBtn.addEventListener("click", resetAndHideForm);

// Real-time validation for task form
document.getElementById("task_title").addEventListener("input", function() {
    const title = this.value.trim();
    if (!title) {
        this.setCustomValidity("Task title is required.");
    } else if (!validateTaskTitle(title)) {
        this.setCustomValidity("Task title must be 1-200 characters long.");
    } else {
        this.setCustomValidity("");
    }
});

document.getElementById("task_description").addEventListener("input", function() {
    const description = this.value.trim();
    if (!validateTaskDescription(description)) {
        this.setCustomValidity("Task description must be 1000 characters or less.");
    } else {
        this.setCustomValidity("");
    }
});

function populateTaskForm(task) {
    clearFormError();
    formTitle.textContent = "Edit Task";
    taskIdField.value = task.id;
    document.getElementById("task_title").value = task.title;
    document.getElementById("task_description").value = task.description || "";
    document.getElementById("assigned_to").value = task.assigned_to || "";
    document.getElementById("task_status").value = task.status;
    document.getElementById("task_priority").value = task.priority;
    document.getElementById("due_date").value = formatDateForInput(task.due_date);
    cancelBtn.style.display = "inline-block";
    taskForm.scrollIntoView({ behavior: 'smooth' });
}

// --- Data Loading ---
async function loadUsers() {
    try {
        // only fetch active users; previously this returned everyone which meant
        // deleted/inactive accounts could be assigned to tasks
        const users = await apiRequest("/users?is_active=true");
        const select = document.getElementById("assigned_to");
        select.innerHTML = `<option value="">-- Unassigned --</option>`;
        users.forEach(u => {
            usersMap[u.id] = u.username;
            const option = document.createElement("option");
            option.value = u.id;
            option.textContent = u.username;
            select.appendChild(option);
        });
    } catch (err) {
        // Non-critical, but log it
        console.error("Failed to load users for assignment:", err);
    }
}

async function loadProjectDetails() {
    projectInfoCard.innerHTML = "<p>Loading project details...</p>";
    try {
        const project = await apiRequest(`/projects/${projectId}`);
        projectInfoCard.innerHTML = `
            <div class="page-header" style="margin-bottom: 8px;">
                <h1>${project.title}</h1>
                <span class="badge ${getStatusBadge(project.status)}">${project.status}</span>
            </div>
            <p class="text-muted" style="margin-bottom: 24px;">${project.description || "No description provided."}</p>
            <div class="grid" style="grid-template-columns: 1fr 1fr; gap: 16px; font-size: 0.9rem;">
                <div>
                    <strong class="text-muted">Start Date</strong>
                    <p style="margin:0;">${formatDate(project.start_date)}</p>
                </div>
                <div>
                    <strong class="text-muted">End Date</strong>
                    <p style="margin:0;">${formatDate(project.end_date)}</p>
                </div>
            </div>
        `;

    // hide task creation controls for non-managers
    const taskFormCard = taskForm.closest('.card');
    if (currentRole !== "manager" && taskFormCard) {
        taskFormCard.style.display = "none";
    }
    } catch (error) {
        showError(projectInfoCard, "Could not load project details: " + error.message);
        setTimeout(() => window.location.href = "projects.html", 2000);
    }
}

async function loadTasks() {
    tasksGrid.innerHTML = `<div>Loading tasks...</div>`;
    try {
        const tasks = await apiRequest(`/tasks?project_id=${projectId}`);
        tasksGrid.innerHTML = ""; // Clear loading message

        const tableCard = document.createElement('div');
        tableCard.className = 'table-card';
        
        const header = document.createElement('h2');
        header.textContent = 'Tasks';
        tableCard.appendChild(header);

        if (tasks.length === 0) {
            tableCard.innerHTML += "<div style='padding: 16px;'><p>No tasks in this project yet. Create one!</p></div>";
            tasksGrid.appendChild(tableCard);
            return;
        }

        const table = document.createElement('table');
        table.className = 'table';
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Task</th>
                    <th>Assigned To</th>
                    <th>Status</th>
                    <th>Priority</th>
                    <th>Due Date</th>
                    <th style="width: 120px;">Actions</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        `;

        const tbody = table.querySelector('tbody');
        tasks.forEach(task => {
            const tr = document.createElement("tr");
            tr.style.cursor = "pointer";
            tr.onclick = (event) => {
                // Only navigate if the click is not on an action button
                if (!event.target.closest('.btn')) {
                    window.location.href = `task-details.html?id=${task.id}`;
                }
            };

            const assigneeName = task.assigned_to
                ? `<a href="user-details.html?id=${task.assigned_to}">${usersMap[task.assigned_to] || "User #" + task.assigned_to}</a>`
                : '<em class="text-muted">Unassigned</em>';

            tr.innerHTML = `
                <td>
                    <strong>${task.title}</strong>
                    <p class="text-muted" style="font-size:0.85rem; margin-bottom: 0;">${(task.description || "").substring(0,50)}</p>
                </td>
                <td>${assigneeName}</td>
                <td><span class="badge ${getStatusBadge(task.status)}">${task.status}</span></td>
                <td><span class="badge ${getPriorityBadge(task.priority)}">${task.priority}</span></td>
                <td>${formatDate(task.due_date)}</td>
            `;

            const actionsCell = document.createElement('td');
            actionsCell.style.whiteSpace = 'nowrap';
            
            // manager-only actions
            if (currentRole === "manager") {
                const editBtn = document.createElement('button');
                editBtn.className = 'btn btn-outline btn-sm';
                editBtn.innerHTML = 'Edit';
                editBtn.style.marginRight = '8px';
                editBtn.onclick = (event) => {
                    event.stopPropagation(); // Prevent row click from firing
                    populateTaskForm(task);
                };
                actionsCell.appendChild(editBtn);

                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'btn btn-danger btn-sm';
                deleteBtn.innerHTML = 'Delete';
                deleteBtn.onclick = async (event) => {
                    event.stopPropagation();
                    if (!confirm("Delete this task?")) return;
                    try {
                        await apiRequest(`/tasks/${task.id}`, "DELETE");
                        loadTasks();
                    } catch (err) {
                        alert("Error deleting task: " + err.message);
                    }
                };
                actionsCell.appendChild(deleteBtn);
            }

            tr.appendChild(actionsCell);

            tbody.appendChild(tr);
        });

        tableCard.appendChild(table);
        tasksGrid.appendChild(tableCard);

    } catch (error) {
        showError(tasksGrid, "Error loading tasks: " + error.message);
    }
}

// --- Action Handlers ---
window.deleteTask = async function(id) {
    if (!confirm("Are you sure you want to delete this task?")) return;
    try {
        await apiRequest(`/tasks/${id}`, "DELETE");
        loadTasks();
    } catch (err) {
        alert("Error deleting task: " + err.message); // Alert is ok for confirm actions
    }
};

taskForm.addEventListener("submit", async function(e) {
    e.preventDefault();
    clearFormError();
    const taskId = taskIdField.value;
    const title = document.getElementById("task_title").value.trim();
    const description = document.getElementById("task_description").value.trim();
    const assignedToVal = document.getElementById("assigned_to").value;

    // Client-side validation
    if (!title) {
        showFormError("Task title is required.");
        return;
    }
    if (!validateTaskTitle(title)) {
        showFormError("Task title must be 1-200 characters long.");
        return;
    }
    if (!validateTaskDescription(description)) {
        showFormError("Task description must be 1000 characters or less.");
        return;
    }

    const payload = {
        title,
        description: description || null,
        status: document.getElementById("task_status").value,
        priority: document.getElementById("task_priority").value,
        due_date: document.getElementById("due_date").value || null,
        project_id: Number(projectId),
        assigned_to: assignedToVal ? Number(assignedToVal) : null
    };

    if(payload.due_date) payload.due_date = new Date(payload.due_date).toISOString();

    const method = taskId ? "PUT" : "POST";
    const endpoint = taskId ? `/tasks/${taskId}` : "/tasks";

    try {
        await apiRequest(endpoint, method, payload);
        resetAndHideForm();
        loadTasks();
    } catch (err) {
        let errorMsg = err.message;
        if (err.status === 400) {
            errorMsg = "Invalid task data. Please check your inputs.";
        } else if (err.status === 403) {
            errorMsg = "You don't have permission to modify this task.";
        } else if (err.status >= 500) {
            errorMsg = "Server error. Please try again later.";
        }
        showFormError("Error saving task: " + errorMsg);
    }
});


// --- Initial Load ---
async function init() {
    // Fire off fetches in a way that allows parallelism but ensures users are loaded first
    await loadUsers();
    loadProjectDetails();
    loadTasks();
}

init();
