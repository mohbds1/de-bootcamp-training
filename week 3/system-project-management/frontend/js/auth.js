function saveAuth(token, user) {
  localStorage.setItem("token", token);
  localStorage.setItem("user_role", user.role);
  localStorage.setItem("username", user.username);
  localStorage.setItem("user_email", user.email);
  // remember the numeric id so front‑end can check assignments
  if (user.id !== undefined && user.id !== null) {
    localStorage.setItem("user_id", String(user.id));
  }
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user_role");
  localStorage.removeItem("username");
  localStorage.removeItem("user_email");
  localStorage.removeItem("user_id");
  window.location.href = "login.html";
}

function requireAuth() {
  const token = localStorage.getItem("token");
  if (!token) {
    window.location.href = "login.html";
  }
}

// دالة لحماية صفحات المدير
function requireManager() {
  requireAuth();
  const role = localStorage.getItem("user_role");
  if (role !== "manager") {
    // توجيه الموظف إذا حاول الدخول لصفحات المدير
    window.location.href = "my-tasks.html";
  }
}

// دالة لحماية صفحات الموظف
function requireEmployee() {
  requireAuth();
  const role = localStorage.getItem("user_role");
  if (role !== "employee") {
    // توجيه المدير إذا حاول الدخول لصفحة مهام الموظف
    window.location.href = "manager-dashboard.html";
  }
}

function goAfterLogin(role) {
  if (role === "manager") {
    window.location.href = "manager-dashboard.html";
  } else {
    window.location.href = "my-tasks.html";
  }
}

function fillNavbarUser() {
  const el = document.getElementById("nav-user");
  const role = localStorage.getItem("user_role") || "";
  if (el) {
    const username = localStorage.getItem("username") || "User";
    el.innerHTML = role
      ? `<span class="nav-username">${username}</span><span class="nav-role-badge">${role}</span>`
      : `<span class="nav-username">${username}</span>`;
  }

  // hide or show navigation links depending on role
  const navDashboard = document.getElementById("nav-dashboard");
  const navProjects = document.getElementById("nav-projects");
  const navUsers = document.getElementById("nav-users");
  const navMyTasks = document.getElementById("nav-my-tasks");

  if (role === "manager") {
    // managers shouldn't see their own My Tasks link
    if (navMyTasks) navMyTasks.style.display = "none";
    if (navDashboard) navDashboard.style.display = "inline";
    if (navUsers) navUsers.style.display = "inline";
  } else if (role === "employee") {
    // employees only need Projects and My Tasks
    if (navDashboard) navDashboard.style.display = "none";
    if (navUsers) navUsers.style.display = "none";
    if (navMyTasks) navMyTasks.style.display = "inline";
  } else {
    // not logged in or unknown role: hide everything but projects
    if (navDashboard) navDashboard.style.display = "none";
    if (navUsers) navUsers.style.display = "none";
    if (navMyTasks) navMyTasks.style.display = "none";
  }
}