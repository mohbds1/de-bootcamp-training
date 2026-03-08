requireEmployee();
fillNavbarUser();

document.getElementById("logoutBtn").addEventListener("click", logout);

const container = document.getElementById("myTasksList");
const errorMessageDiv = document.getElementById("errorMessage");

// hide Users link if any (redundant but safe)
const navUsers = document.getElementById("nav-users");
if (navUsers) navUsers.style.display = "none";

// --- Helper Functions ---
function showError(message) {
    errorMessageDiv.textContent = message;
    errorMessageDiv.style.display = "block";
    container.innerHTML = ""; // Clear any previous content
}

function clearError() {
    errorMessageDiv.textContent = "";
    errorMessageDiv.style.display = "none";
}

function getStatusBadge(status) {
    const statusMap = {
        completed: "badge-success",
        in_progress: "badge-info",
        todo: "badge-warning",
    };
    return statusMap[status] || "badge-gray";
}

function getPriorityBadge(priority) {
    const priorityMap = {
        high: "badge-danger",
        medium: "badge-warning",
        low: "badge-info",
    };
    return priorityMap[priority] || "badge-gray";
}


function formatDate(dateString) {
    if (!dateString) return "N/A";
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// --- Main Load Function ---
async function loadMyTasks() {
    clearError();
    container.innerHTML = "<div class='card'>Loading your tasks...</div>";

    try {
        // The backend /tasks endpoint automatically returns tasks for the current user if they are an employee
        const tasks = await apiRequest("/tasks");
        container.innerHTML = ""; // Clear loading message

        if (tasks.length === 0) {
            container.innerHTML = "<div class='card'><p>No tasks assigned to you. Great job!</p></div>";
            return;
        }

        tasks.forEach(task => {
            const card = document.createElement("div");
            card.className = "card";
            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <h3 style="margin-bottom: 8px;">${task.title}</h3>
                    <span class="badge ${getPriorityBadge(task.priority)}">${task.priority}</span>
                </div>
                <p class="text-muted">${task.description || "No description."}</p>
                <div style="margin-top: 16px;">
                    <p><strong>Status:</strong> <span class="badge ${getStatusBadge(task.status)}">${task.status}</span></p>
                    <p><strong>Project ID:</strong> ${task.project_id}</p>
                    <p><strong>Due Date:</strong> ${formatDate(task.due_date)}</p>
                </div>
                <div style="margin-top: 16px;">
                    <a href="task-details.html?id=${task.id}" class="btn btn-primary">View/Edit Task</a>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (err) {
        showError(`Failed to load tasks: ${err.message}`);
    }
}

loadMyTasks();
