document.getElementById("loginForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const username_or_email = document.getElementById("username_or_email").value.trim();
  const password = document.getElementById("password").value;
  const message = document.getElementById("message");

  message.textContent = "";
  message.style.color = "red";

  // Client-side validation
  if (!username_or_email) {
    message.textContent = "Please enter your username or email.";
    return;
  }
  if (!password) {
    message.textContent = "Please enter your password.";
    return;
  }

  try {
    const loginResult = await apiRequest("/auth/login", "POST", {
      username_or_email,
      password
    }, false);

    if (!loginResult || !loginResult.access_token) {
      throw new Error("Login succeeded but token was not returned.");
    }

    localStorage.setItem("token", loginResult.access_token);

    const me = await apiRequest("/auth/me", "GET", null, true);

    if (!me || !me.role) {
      throw new Error("Could not load user profile after login.");
    }

    saveAuth(loginResult.access_token, me);
    goAfterLogin(me.role);

  } catch (error) {
    let errorMsg = error.message;
    if (error.status === 401) {
      errorMsg = "Invalid username/email or password. Please try again.";
    } else if (error.status >= 500) {
      errorMsg = "Server error. Please try again later.";
    }
    message.style.color = "red";
    message.textContent = errorMsg;
    console.error("Login error:", error);
  }
});