// Initial auth checks and navbar setup
requireManager();
fillNavbarUser();
document.getElementById("logoutBtn").addEventListener("click", logout);

// --- Globals ---
const params = new URLSearchParams(window.location.search);
const userId = params.get("id");
if (!userId) {
    alert("No user ID provided!");
    window.location.href = "users.html";
}

// --- DOM Elements ---
const userInfoCard = document.getElementById("userInfoCard");
const assignedTasksContainer = document.getElementById("assignedTasks");
const participatingProjectsContainer = document.getElementById("participatingProjects");

// --- Helper Functions ---
function getStatusBadge(status) {
    const map = { completed: "badge-success", in_progress: "badge-info", todo: "badge-warning" };
    return map[status] || "badge-gray";
}

function formatDate(dateString) {
    if (!dateString) return "N/A";
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// --- Data Rendering ---
function renderUserInfo(user) {
    userInfoCard.innerHTML = `
        <div class="page-header" style="margin-bottom: 8px;">
            <h1>${user.full_name || user.username}</h1>
            <span class="badge ${user.is_active ? 'badge-success' : 'badge-danger'}">
                ${user.is_active ? 'Active' : 'Inactive'}
            </span>
        </div>
        <p class="text-muted" style="margin-bottom: 24px;">${user.email} | Role: ${user.role}</p>
        <p>Member since: ${formatDate(user.created_at)}</p>
    `;
}

function renderTasks(tasks) {
    const tableCard = document.createElement('div');
    tableCard.className = 'table-card';
    tableCard.innerHTML = '<h2>Assigned Tasks</h2>';

    if (tasks.length === 0) {
        tableCard.innerHTML += `<div style="padding: 16px;"><p>No tasks assigned to this user.</p></div>`;
        assignedTasksContainer.innerHTML = '';
        assignedTasksContainer.appendChild(tableCard);
        return;
    }

    const table = document.createElement('table');
    table.className = 'table';
    table.innerHTML = `
        <thead>
            <tr>
                <th>Task</th>
                <th>Status</th>
                <th>Due Date</th>
            </tr>
        </thead>
        <tbody>
            ${tasks.map(task => `
                <tr style="cursor: pointer;" onclick="window.location.href='task-details.html?id=${task.id}'">
                    <td>${task.title}</td>
                    <td><span class="badge ${getStatusBadge(task.status)}">${task.status}</span></td>
                    <td>${formatDate(task.due_date)}</td>
                </tr>
            `).join('')}
        </tbody>
    `;
    tableCard.appendChild(table);
    assignedTasksContainer.innerHTML = '';
    assignedTasksContainer.appendChild(tableCard);
}

function renderProjects(projects) {
    const tableCard = document.createElement('div');
    tableCard.className = 'table-card';
    tableCard.innerHTML = '<h2>Participating Projects</h2>';

    if (projects.length === 0) {
        tableCard.innerHTML += `<div style="padding: 16px;"><p>This user is not participating in any projects.</p></div>`;
        participatingProjectsContainer.innerHTML = '';
        participatingProjectsContainer.appendChild(tableCard);
        return;
    }

    const table = document.createElement('table');
    table.className = 'table';
    table.innerHTML = `
        <thead>
            <tr>
                <th>Project</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            ${projects.map(project => `
                <tr style="cursor: pointer;" onclick="window.location.href='project-details.html?id=${project.id}'">
                    <td>${project.title}</td>
                    <td><span class="badge ${getStatusBadge(project.status)}">${project.status}</span></td>
                </tr>
            `).join('')}
        </tbody>
    `;
    tableCard.appendChild(table);
    participatingProjectsContainer.innerHTML = '';
    participatingProjectsContainer.appendChild(tableCard);
}


// --- Main Load Function ---
async function loadUserDetails() {
    try {
        // Fetch all data in parallel
        const [user, tasks, projects] = await Promise.all([
            apiRequest(`/users/${userId}`),
            apiRequest(`/users/${userId}/tasks`),
            apiRequest(`/users/${userId}/projects`)
        ]);

        // Render all components
        renderUserInfo(user);
        renderTasks(tasks);
        renderProjects(projects);

    } catch (err) {
        console.error("Failed to load user details:", err);
        userInfoCard.innerHTML = `<div class="error-message">Failed to load user details: ${err.message}</div>`;
    }
}

loadUserDetails();
