// Initial auth checks and navbar setup
// An employee can view a task if they are assigned to it, so we only require authentication (any role).
requireAuth();
fillNavbarUser();
document.getElementById("logoutBtn").addEventListener("click", logout);

// --- Globals ---
const params = new URLSearchParams(window.location.search);
const taskId = params.get("id");
if (!taskId) {
    alert("No task ID provided!");
    window.location.href = "manager-dashboard.html";
}

// --- DOM Elements ---
const taskInfoCard = document.getElementById("taskInfoCard");
const statusUpdateCard = document.getElementById("statusUpdateCard");
const statusForm = document.getElementById("statusForm");
const statusSelect = document.getElementById("task_status");
const statusError = document.getElementById("statusError");

// --- Helper Functions ---
function getStatusBadge(status) {
    const map = { completed: "badge-success", in_progress: "badge-info", todo: "badge-warning" };
    return map[status] || "badge-gray";
}
function getPriorityBadge(priority) {
    const map = { high: "badge-danger", medium: "badge-warning", low: "badge-info" };
    return map[priority] || "badge-gray";
}
function formatDate(dateString) {
    if (!dateString) return "N/A";
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// --- Data Rendering ---
function renderTaskDetails(task, project, user) {
    const projectName = project ? `<a href="project-details.html?id=${project.id}">${project.title}</a>` : 'N/A';
    let userName;
    if (user) {
        // manager has permission to view full user profile
        userName = `<a href="user-details.html?id=${user.id}">${user.full_name || user.username}</a>`;
    } else if (task.assigned_to_username) {
        // we know the name from the task response so just render plain text
        userName = `<span>${task.assigned_to_username}</span>`;
    } else {
        userName = '<span class="text-muted">Unassigned</span>';
    }

    taskInfoCard.innerHTML = `
        <div class="page-header" style="margin-bottom: 8px;">
            <h1 style="font-size: 1.8rem;">${task.title}</h1>
            <span class="badge ${getPriorityBadge(task.priority)}">${task.priority} Priority</span>
        </div>

        <div style="margin-bottom: 24px;">
            <span class="badge ${getStatusBadge(task.status)}">${task.status}</span>
        </div>

        <p class="text-muted" style="font-size: 1.1rem;">${task.description || "No description provided."}</p>

        <div style="border-top: 1px solid var(--border-color); margin-top: 24px; padding-top: 24px;">
            <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 16px;">
                <div>
                    <strong class="text-muted">Project</strong>
                    <p style="margin:0;">${projectName}</p>
                </div>
                <div>
                    <strong class="text-muted">Assigned To</strong>
                    <p style="margin:0;">${userName}</p>
                </div>
                <div>
                    <strong class="text-muted">Due Date</strong>
                    <p style="margin:0;">${formatDate(task.due_date)}</p>
                </div>
                 <div>
                    <strong class="text-muted">Created</strong>
                    <p style="margin:0;">${formatDate(task.created_at)}</p>
                </div>
            </div>
        </div>
    `;

    // Show status update form if user is employee and assigned to this task
    const currentRole = localStorage.getItem("user_role");
    const currentUserId = parseInt(localStorage.getItem("user_id"));
    if (currentRole === "employee" && task.assigned_to === currentUserId) {
        statusSelect.value = task.status;
        statusUpdateCard.style.display = "block";
    } else {
        statusUpdateCard.style.display = "none";
    }
}

// --- Main Load Function ---
async function loadTaskDetails() {
    try {
        const task = await apiRequest(`/tasks/${taskId}`);

        // After getting the task, fetch project info if available
        let project = null;
        if (task.project_id) {
            try {
                project = await apiRequest(`/projects/${task.project_id}`);
            } catch (projErr) {
                console.warn("Unable to load project info for task:", projErr);
            }
        }

        // user details no longer requested; frontend uses `assigned_to_username` field
        renderTaskDetails(task, project, null);

    } catch (err) {
        console.error("Failed to load task details:", err);
        let message = "Failed to load task details.";
        if (err.status === 403) {
            // distinguish between task permission and other problems
            message = "You are not authorized to view this task. Only its assignee or a manager can open it.";
        }
        taskInfoCard.innerHTML = `<div class="error-message">${message} (${err.message})</div>`;
    }
}

// --- Status Update Handler ---
statusForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    statusError.style.display = "none";
    const newStatus = statusSelect.value;

    try {
        await apiRequest(`/tasks/${taskId}/status`, "PATCH", { status: newStatus });
        // Reload the task details to reflect the change
        loadTaskDetails();
        alert("Task status updated successfully!");
    } catch (err) {
        statusError.textContent = `Failed to update status: ${err.message}`;
        statusError.style.display = "block";
    }
});

loadTaskDetails();
