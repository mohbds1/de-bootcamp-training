document.getElementById("registerForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const message = document.getElementById("message");

  message.textContent = "";
  message.style.color = "red";

  // Client-side validation
  if (!username) {
    message.textContent = "Username is required.";
    return;
  }
  if (!validateUsername(username)) {
    message.textContent = "Username must be 3-50 characters long and contain only letters, numbers, and underscores.";
    return;
  }
  if (!email) {
    message.textContent = "Email is required.";
    return;
  }
  if (!validateEmail(email)) {
    message.textContent = "Please enter a valid email address.";
    return;
  }
  if (!password) {
    message.textContent = "Password is required.";
    return;
  }
  if (!validatePassword(password)) {
    message.textContent = "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.";
    return;
  }

  try {
    await apiRequest(
      "/auth/register",
      "POST",
      {
        username,
        email,
        password
      },
      false
    );

    message.style.color = "green";
    message.textContent = "Registration successful. Redirecting to login...";

    setTimeout(() => {
      window.location.href = "login.html";
    }, 1200);
  } catch (error) {
    let errorMsg = error.message;
    if (error.status === 409) {
      errorMsg = "Username or email already exists. Please choose different ones.";
    } else if (error.status === 400) {
      errorMsg = "Invalid registration data. Please check your inputs.";
    } else if (error.status >= 500) {
      errorMsg = "Server error. Please try again later.";
    }
    message.style.color = "red";
    message.textContent = errorMsg;
  }
});

// Validation functions
function validateUsername(username) {
  return /^[a-zA-Z0-9_]{3,50}$/.test(username);
}

function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validatePassword(password) {
  return password.length >= 8 &&
         /[a-z]/.test(password) &&
         /[A-Z]/.test(password) &&
         /\d/.test(password);
}

// Real-time validation for register form
document.getElementById("username").addEventListener("input", function() {
  const username = this.value.trim();
  if (!username) {
    this.setCustomValidity("Username is required.");
  } else if (!validateUsername(username)) {
    this.setCustomValidity("Username must be 3-50 characters long and contain only letters, numbers, and underscores.");
  } else {
    this.setCustomValidity("");
  }
});

document.getElementById("email").addEventListener("input", function() {
  const email = this.value.trim();
  if (!email) {
    this.setCustomValidity("Email is required.");
  } else if (!validateEmail(email)) {
    this.setCustomValidity("Please enter a valid email address.");
  } else {
    this.setCustomValidity("");
  }
});

document.getElementById("password").addEventListener("input", function() {
  const password = this.value;
  if (!password) {
    this.setCustomValidity("Password is required.");
  } else if (!validatePassword(password)) {
    this.setCustomValidity("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.");
  } else {
    this.setCustomValidity("");
  }
});