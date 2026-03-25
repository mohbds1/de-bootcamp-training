requireManager();
fillNavbarUser();

document.getElementById("logoutBtn").addEventListener("click", logout);

const errorMessageDiv = document.getElementById("errorMessage");

// --- Helper Functions ---
function showError(message) {
    errorMessageDiv.textContent = message;
    errorMessageDiv.style.display = "block";
}

function clearError() {
    errorMessageDiv.textContent = "";
    errorMessageDiv.style.display = "none";
}

function getStatusBadge(status) {
    switch (status) {
        case "completed": return "badge-success";
        case "active": case "in_progress": return "badge-info";
        case "planned": case "todo": return "badge-warning";
        default: return "badge-gray";
    }
}

function formatDate(dateString) {
    if (!dateString) return "N/A";
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function setInitialLoadingState() {
    const loadingRowProjects = '<tr><td colspan="4" style="text-align: center;">Loading...</td></tr>';
    const loadingRowTasks = '<tr><td colspan="4" style="text-align: center;">Loading...</td></tr>';
    document.getElementById("recentProjectsTableBody").innerHTML = loadingRowProjects;
    document.getElementById("recentTasksTableBody").innerHTML = loadingRowTasks;

    const counts = ["projectsCount", "tasksCount", "completedCount", "inProgressCount", "todoCount"];
    counts.forEach(id => document.getElementById(id).textContent = "...");
}

// --- Data Population ---
function populateRecentProjects(projects) {
    const tableBody = document.getElementById("recentProjectsTableBody");
    const recentProjects = projects.slice(0, 5);

    if (recentProjects.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="4" style="text-align: center;">No projects found.</td></tr>';
        return;
    }
    
    tableBody.innerHTML = ""; // Clear loading state
    recentProjects.forEach(project => {
        const tr = document.createElement("tr");
        tr.style.cursor = "pointer";
        tr.addEventListener("click", () => window.location.href = `project-details.html?id=${project.id}`);

        tr.innerHTML = `
            <td>${project.title}</td>
            <td><span class="badge ${getStatusBadge(project.status)}">${project.status}</span></td>
            <td>${formatDate(project.end_date)}</td>
            <td><a href="project-details.html?id=${project.id}" class="btn btn-outline btn-sm">Open</a></td>
        `;
        tableBody.appendChild(tr);
    });
}

function populateRecentTasks(tasks, projectMap) {
    const tableBody = document.getElementById("recentTasksTableBody");
    const recentTasks = tasks.slice(0, 5);

    if (recentTasks.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="4" style="text-align: center;">No tasks found.</td></tr>';
        return;
    }

    tableBody.innerHTML = ""; // Clear loading state
    recentTasks.forEach(task => {
        const tr = document.createElement("tr");
        const projectName = projectMap.get(task.project_id)?.title || 'Unknown';
        tr.innerHTML = `
            <td>${task.title}</td>
            <td>${projectName}</td>
            <td><span class="badge ${getStatusBadge(task.status)}">${task.status}</span></td>
            <td>${formatDate(task.due_date)}</td>
        `;
        tableBody.appendChild(tr);
    });
}

// --- Main Load Function ---
async function loadDashboard() {
    clearError();
    setInitialLoadingState();

    try {
        // Fetch data in parallel
        const [projects, tasks] = await Promise.all([
            apiRequest("/projects"),
            apiRequest("/tasks")
        ]);

        // Create a map for quick project title lookup
        const projectMap = new Map(projects.map(p => [p.id, p]));

        // Populate summary counts
        document.getElementById("projectsCount").textContent = projects.length;
        document.getElementById("tasksCount").textContent = tasks.length;
        document.getElementById("completedCount").textContent = tasks.filter(t => t.status === "completed").length;
        document.getElementById("inProgressCount").textContent = tasks.filter(t => t.status === "in_progress").length;
        document.getElementById("todoCount").textContent = tasks.filter(t => t.status === "todo").length;
        
        // Populate recent items tables
        populateRecentProjects(projects);
        populateRecentTasks(tasks, projectMap);

    } catch (err) {
        showError("Failed to load dashboard: " + err.message);
        console.error(err);
    }
}

loadDashboard();
