console.log("users.js loaded");
requireManager();
fillNavbarUser();

document.getElementById("logoutBtn").addEventListener("click", logout);

const usersTableBody = document.getElementById("usersTableBody");

// Form-related elements
const userFormCard = document.getElementById("userFormCard");
const userForm = document.getElementById("userForm");
const userFormTitle = document.getElementById("userFormTitle");
const userFormError = document.getElementById("userFormError");
// submit button used to show loading state
const saveUserBtn = userForm.querySelector('button[type="submit"]');
const userIdField = document.getElementById("userId");
const newUserBtn = document.getElementById("newUserBtn");
const cancelUserBtn = document.getElementById("cancelUserBtn");
const usernameInput = document.getElementById("user_username");
const emailInput = document.getElementById("user_email");
const fullNameInput = document.getElementById("user_full_name");
const passwordRow = document.getElementById("passwordRow");
const passwordInput = document.getElementById("user_password");
const isActiveRow = document.getElementById("isActiveRow");
const isActiveSelect = document.getElementById("user_is_active");
const roleRow = document.getElementById("roleRow");
const roleSelect = document.getElementById("user_role");

function getRoleBadge(role) {
    if (role === "manager") {
        return "badge-info";
    }
    return "badge-gray";
}

function getStatusBadge(isActive) {
    if (isActive) {
        return "badge-success";
    }
    return "badge-danger";
}

function showTableError(message) {
    usersTableBody.innerHTML = `<tr><td colspan="6" class="error-message" style="text-align: center; padding: 16px;">${message}</td></tr>`;
}

function clearUserFormError() {
    userFormError.textContent = "";
    userFormError.style.color = "red";
    userFormError.style.display = "none";
}

function showUserFormError(message) {
    userFormError.style.color = "red";
    userFormError.textContent = message;
    userFormError.style.display = "block";
}

function showUserFormSuccess(message) {
    userFormError.style.color = "green";
    userFormError.textContent = message;
    userFormError.style.display = "block";
}

// Validation functions
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validateUsername(username) {
    return username.length >= 3 && username.length <= 50;
}

function validatePassword(password) {
    return password.length >= 6;
}

// Real-time validation
usernameInput.addEventListener("input", () => {
    if (usernameInput.value && !validateUsername(usernameInput.value)) {
        usernameInput.setCustomValidity("Username must be 3-50 characters long.");
    } else {
        usernameInput.setCustomValidity("");
    }
});

emailInput.addEventListener("input", () => {
    if (emailInput.value && !validateEmail(emailInput.value)) {
        emailInput.setCustomValidity("Please enter a valid email address.");
    } else {
        emailInput.setCustomValidity("");
    }
});

if (passwordInput) {
    passwordInput.addEventListener("input", () => {
        if (passwordInput.value && !validatePassword(passwordInput.value)) {
            passwordInput.setCustomValidity("Password must be at least 6 characters long.");
        } else {
            passwordInput.setCustomValidity("");
        }
    });
}

function showUserForm(isEdit = false, user = null) {
    clearUserFormError();
    userForm.reset();
    userIdField.value = "";

    if (isEdit && user) {
        userFormTitle.textContent = "Edit User";
        userIdField.value = user.id;
        usernameInput.value = user.username;
        emailInput.value = user.email;
        fullNameInput.value = user.full_name || "";
        roleSelect.value = user.role;
        isActiveSelect.value = user.is_active ? "true" : "false";
        // hide and disable password field when editing so validation doesn't block submit
        passwordRow.style.display = "none";
        passwordInput.required = false;
        passwordInput.minLength = 0;
        passwordInput.value = ""; // clear any leftover
        passwordInput.disabled = true;
        roleRow.style.display = "block";
        isActiveRow.style.display = "block";
    } else {
        userFormTitle.textContent = "Create User";
        passwordRow.style.display = "block";
        passwordInput.required = true;
        passwordInput.minLength = 6;
        passwordInput.disabled = false;
        roleRow.style.display = "none";
        isActiveRow.style.display = "none";
    }

    userFormCard.style.display = "block";
    document.getElementById("usersListSection").style.display = "none";
    window.scrollTo({ top: 0, behavior: "smooth" });
}

function hideUserForm() {
    clearUserFormError();
    userForm.reset();
    userIdField.value = "";
    userFormCard.style.display = "none";
    document.getElementById("usersListSection").style.display = "block";
}

newUserBtn.addEventListener("click", () => showUserForm(false));
cancelUserBtn.addEventListener("click", hideUserForm);
document.getElementById("applyUserFilters").addEventListener("click", () => loadUsers());
document.getElementById("userSearch").addEventListener("keypress", (e) => {
    if (e.key === "Enter") loadUsers();
});

function buildUsersQuery() {
    const params = new URLSearchParams();
    params.set("limit", "100");
    const search = document.getElementById("userSearch").value.trim();
    const role = document.getElementById("userRoleFilter").value;
    const isActive = document.getElementById("userStatusFilter").value;
    if (search) params.set("search", search);
    if (role) params.set("role", role);
    // if the filter dropdown has a value, use it; otherwise default to active
    // users only.  The backend returns all users when the parameter is absent
    // because soft-deleted users are kept with is_active=False.
    if (isActive) {
        params.set("is_active", isActive);
    } else {
        params.set("is_active", "true");
    }
    const qs = params.toString();
    return qs ? `/users?${qs}` : "/users?limit=100";
}

async function loadUsers() {
    usersTableBody.innerHTML = `<tr><td colspan="6" style="text-align: center; padding: 16px;">Loading...</td></tr>`;
    try {
        const users = await apiRequest(buildUsersQuery());
        usersTableBody.innerHTML = "";

        if (users.length === 0) {
            usersTableBody.innerHTML = '<tr><td colspan="6" style="text-align: center;">No users found.</td></tr>';
            return;
        }

        users.forEach(user => {
            const tr = document.createElement("tr");
            tr.style.cursor = "pointer";
            tr.onclick = () => {
                window.location.href = `user-details.html?id=${user.id}`;
            };

            const activeStatus = user.is_active ? "Active" : "Inactive";
            tr.innerHTML = `
                <td>${user.id}</td>
                <td>${user.full_name || user.username}</td>
                <td>${user.email}</td>
                <td><span class="badge ${getRoleBadge(user.role)}">${user.role}</span></td>
                <td><span class="badge ${getStatusBadge(user.is_active)}">${activeStatus}</span></td>
            `;

            const actionsTd = document.createElement("td");
            actionsTd.style.whiteSpace = "nowrap";

            const editBtn = document.createElement("button");
            editBtn.className = "btn btn-outline btn-sm";
            editBtn.textContent = "Edit";
            editBtn.onclick = (event) => {
                event.stopPropagation();
                showUserForm(true, user);
            };

            const deleteBtn = document.createElement("button");
            deleteBtn.className = "btn btn-danger btn-sm";
            deleteBtn.textContent = "Delete";
            deleteBtn.style.marginLeft = "8px";
            deleteBtn.onclick = async (event) => {
                event.stopPropagation();
                if (!confirm("Are you sure you want to delete this user?")) return;
                try {
                    await apiRequest(`/users/${user.id}`, "DELETE");
                    loadUsers();
                } catch (error) {
                    alert("Error deleting user: " + error.message);
                }
            };

            actionsTd.appendChild(editBtn);
            actionsTd.appendChild(deleteBtn);
            tr.appendChild(actionsTd);

            usersTableBody.appendChild(tr);
        });
    } catch (error) {
        showTableError("Error loading users: " + error.message);
    }
}

userForm.addEventListener("submit", async function (e) {
    console.log('userForm submit triggered');
    e.preventDefault();
    clearUserFormError();

    const id = userIdField.value;
    const username = usernameInput.value.trim();
    const email = emailInput.value.trim();
    const full_name = fullNameInput.value.trim() || null;

    // Client-side validation
    if (!username) {
        showUserFormError("Username is required.");
        return;
    }
    if (!validateUsername(username)) {
        showUserFormError("Username must be 3-50 characters long.");
        return;
    }
    if (!email) {
        showUserFormError("Email is required.");
        return;
    }
    if (!validateEmail(email)) {
        showUserFormError("Please enter a valid email address.");
        return;
    }
    if (!id && !passwordInput.value) { // Only for new users
        showUserFormError("Password is required for new users.");
        return;
    }
    if (!id && !validatePassword(passwordInput.value)) {
        showUserFormError("Password must be at least 6 characters long.");
        return;
    }

    // disable save button immediately
    if (saveUserBtn) {
        saveUserBtn.disabled = true;
        saveUserBtn.textContent = "Saving...";
    }

    try {
        if (id) {
            const payload = {
                username,
                email,
                full_name,
                role: roleSelect.value,
                is_active: isActiveSelect.value === "true",
            };
            await apiRequest(`/users/${id}`, "PUT", payload);
            showUserFormSuccess("User updated successfully.");
        } else {
            // Create new employee user via /auth/register
            const password = passwordInput.value;
            const payload = {
                username,
                email,
                password,
                full_name,
            };
            await apiRequest("/auth/register", "POST", payload, false);
            showUserFormSuccess("User created successfully.");
        }

        // hide after a brief delay so user sees message
        setTimeout(() => {
            hideUserForm();
            loadUsers();
        }, 800);
    } catch (error) {
        let errorMsg = error.message;
        if (error.status === 409) {
            errorMsg = "Username or email already exists. Please choose different ones.";
        } else if (error.status === 400) {
            errorMsg = "Invalid data provided. Please check your inputs.";
        } else if (error.status >= 500) {
            errorMsg = "Server error. Please try again later.";
        }
        showUserFormError("Error saving user: " + errorMsg);
    } finally {
        if (saveUserBtn) {
            saveUserBtn.disabled = false;
            saveUserBtn.textContent = "Save";
        }
    }
});

loadUsers();
