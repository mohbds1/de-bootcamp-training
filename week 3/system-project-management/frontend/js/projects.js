requireAuth();
fillNavbarUser();

const currentRole = localStorage.getItem("user_role");

document.getElementById("logoutBtn").addEventListener("click", logout);

// --- DOM Elements ---
const projectFormCard = document.getElementById("projectFormCard");
const projectForm = document.getElementById("projectForm");
const projectsGrid = document.getElementById("projectsGrid");
const projectIdField = document.getElementById("projectId");
const newProjectBtn = document.getElementById("newProjectBtn");
const cancelBtn = document.getElementById("cancelBtn");
const formTitle = document.getElementById("formTitle");
const formErrorMessage = document.getElementById("formErrorMessage");

// --- Helper Functions ---
function getStatusBadge(status) {
    switch (status) {
        case "completed": return "badge-success";
        case "active": return "badge-info";
        case "planned": return "badge-warning";
        default: return "badge-gray";
    }
}

function formatDate(dateString) {
    if (!dateString) return "N/A";
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function showGridError(message) {
    projectsGrid.innerHTML = `<div class="card error-message">${message}</div>`;
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
function validateTitle(title) {
    return title.trim().length >= 1 && title.trim().length <= 200;
}

function validateDates(startDate, endDate) {
    if (!startDate && !endDate) return true;
    if (startDate && endDate) {
        return new Date(startDate) <= new Date(endDate);
    }
    return true; // One date is optional
}

// --- UI Toggling ---
function showForm(isEdit = false, project = null) {
    clearFormError();
    formTitle.textContent = isEdit ? "Edit Project" : "Create Project";
    projectForm.reset();
    projectIdField.value = "";

    if (isEdit && project) {
        projectIdField.value = project.id;
        document.getElementById("title").value = project.title;
        document.getElementById("description").value = project.description || "";
        document.getElementById("status").value = project.status;
        document.getElementById("start_date").value = project.start_date ? project.start_date.split('T')[0] : "";
        document.getElementById("end_date").value = project.end_date ? project.end_date.split('T')[0] : "";
    }
    
    projectFormCard.style.display = "block";
    document.getElementById("projectsListSection").style.display = "none";
    window.scrollTo({ top: 0, behavior: "smooth" });
}

function hideForm() {
    clearFormError();
    projectForm.reset();
    projectIdField.value = "";
    projectFormCard.style.display = "none";
    document.getElementById("projectsListSection").style.display = "block";
}

// hide management controls if not manager
if (currentRole !== "manager") {
    newProjectBtn.style.display = "none";
}

if (currentRole === "manager") {
    newProjectBtn.addEventListener("click", () => showForm(false));
    cancelBtn.addEventListener("click", hideForm);
}

// Real-time validation for project form
document.getElementById("title").addEventListener("input", function() {
    const title = this.value.trim();
    if (!title) {
        this.setCustomValidity("Project title is required.");
    } else if (!validateTitle(title)) {
        this.setCustomValidity("Project title must be 1-200 characters long.");
    } else {
        this.setCustomValidity("");
    }
});

document.getElementById("start_date").addEventListener("input", function() {
    const startDate = this.value;
    const endDate = document.getElementById("end_date").value;
    if (!validateDates(startDate, endDate)) {
        this.setCustomValidity("Start date must be before end date.");
    } else {
        this.setCustomValidity("");
    }
});

document.getElementById("end_date").addEventListener("input", function() {
    const startDate = document.getElementById("start_date").value;
    const endDate = this.value;
    if (!validateDates(startDate, endDate)) {
        this.setCustomValidity("End date must be after start date.");
    } else {
        this.setCustomValidity("");
    }
});

document.getElementById("applyProjectFilters").addEventListener("click", () => loadProjects());
document.getElementById("projectSearch").addEventListener("keypress", (e) => {
    if (e.key === "Enter") loadProjects();
});


// --- Data Loading and Rendering ---
function buildProjectsQuery() {
    const params = new URLSearchParams();
    params.set("limit", "100");
    const search = document.getElementById("projectSearch").value.trim();
    const status = document.getElementById("projectStatusFilter").value;
    if (search) params.set("search", search);
    if (status) params.set("status", status);
    const qs = params.toString();
    return qs ? `/projects?${qs}` : "/projects?limit=100";
}

async function loadProjects() {
    projectsGrid.innerHTML = `<div class="card">Loading projects...</div>`;

    try {
        const projects = await apiRequest(buildProjectsQuery());
        projectsGrid.innerHTML = "";

        if (projects.length === 0) {
            projectsGrid.innerHTML = "<div class='card'><p>No projects found. Create one to get started!</p></div>";
            return;
        }

        projects.forEach(project => {
            const card = document.createElement("div");
            card.className = "project-card";
            card.innerHTML = `
                <div class="project-card-content">
                    <h3>${project.title}</h3>
                    <p class="text-muted">${(project.description || "No description provided.").substring(0, 120)}</p>
                </div>
                <div class="project-card-meta">
                    <span class="badge ${getStatusBadge(project.status)}">${project.status}</span>
                    <span class="text-muted">Due: ${formatDate(project.end_date)}</span>
                </div>
                <div class="project-card-footer">
                    <a href="project-details.html?id=${project.id}" class="btn btn-primary">Open</a>
                </div>
            `;
            
            const footer = card.querySelector('.project-card-footer');

            // only managers can edit/delete
            if (currentRole === "manager") {
                const editBtn = document.createElement('button');
                editBtn.className = 'btn btn-outline';
                editBtn.textContent = 'Edit';
                editBtn.onclick = () => editProject(project);
                footer.insertBefore(editBtn, footer.firstChild);

                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'btn btn-danger';
                deleteBtn.textContent = 'Delete';
                deleteBtn.onclick = () => deleteProject(project.id);
                footer.insertBefore(deleteBtn, editBtn);
            }
            
            projectsGrid.appendChild(card);
        });
    } catch (error) {
        showGridError("Error loading projects: " + error.message);
    }
}

// --- Event Handlers for Actions ---
window.editProject = function (project) {
    showForm(true, project);
    window.scrollTo(0, 0);
};

window.deleteProject = async function (id) {
    if (!confirm("Are you sure you want to delete this project? This action cannot be undone.")) return;

    try {
        await apiRequest(`/projects/${id}`, "DELETE");
        hideForm(); // Hide form in case we were editing the deleted project
        loadProjects();
    } catch (error) {
        // Since this is a modal action, an alert is acceptable here for immediate feedback.
        alert("Error deleting project: " + error.message);
    }
};

projectForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    clearFormError();

    const id = projectIdField.value;
    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();
    const status = document.getElementById("status").value;
    const start_date = document.getElementById("start_date").value;
    const end_date = document.getElementById("end_date").value;

    // Client-side validation
    if (!title) {
        showFormError("Project title is required.");
        return;
    }
    if (!validateTitle(title)) {
        showFormError("Project title must be 1-200 characters long.");
        return;
    }
    if (!validateDates(start_date, end_date)) {
        showFormError("End date must be after start date.");
        return;
    }

    const payload = {
        title,
        description: description || null,
        status,
        start_date: start_date || null,
        end_date: end_date || null,
    };
    
    if(payload.start_date) payload.start_date = new Date(payload.start_date).toISOString();
    if(payload.end_date) payload.end_date = new Date(payload.end_date).toISOString();

    try {
        if (id) {
            await apiRequest(`/projects/${id}`, "PUT", payload);
        } else {
            await apiRequest("/projects", "POST", payload);
        }
        hideForm();
        loadProjects();
    } catch (error) {
        let errorMsg = error.message;
        if (error.status === 400) {
            errorMsg = "Invalid project data. Please check your inputs.";
        } else if (error.status >= 500) {
            errorMsg = "Server error. Please try again later.";
        }
        showFormError("Error saving project: " + errorMsg);
    }
});

// Initial Load
loadProjects();
