// frontend/js/api.js
const BASE_URL = "http://127.0.0.1:8000";

function getToken() {
  return localStorage.getItem("token");
}

async function apiRequest(endpoint, method = "GET", data = null, auth = true) {
  const headers = {
    "Content-Type": "application/json"
  };

  if (auth && getToken()) {
    headers["Authorization"] = `Bearer ${getToken()}`;
  }

  const options = {
    method,
    headers
  };

  if (data !== null) {
    options.body = JSON.stringify(data);
  }

  let response;
  try {
    response = await fetch(`${BASE_URL}${endpoint}`, options);
  } catch (networkError) {
    throw new Error("لا يمكن الاتصال بالخادم. تأكد من تشغيل FastAPI على http://127.0.0.1:8000");
  }

  // Handle 401 Unauthorized for expired tokens
  if (response.status === 401) {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "login.html";
    throw new Error("Session expired. Please log in again.");
  }

  let responseData = null;
  // Some endpoints (DELETE, 204 No Content) return an empty body but may still
  // include application/json. Attempting to parse such responses throws the
  // "Unexpected end of JSON input" error that you're seeing in the alert box.
  //
  // Work around this by skipping parsing when the status is 204 or the body is
  // empty, and only call json() when there's something to parse.
  const contentType = response.headers.get("content-type") || "";

  if (response.status === 204) {
    // no content – leave responseData as null
  } else if (contentType.includes("application/json")) {
    // guard against empty body as some servers send a JSON content-type but
    // no payload
    const text = await response.text();
    responseData = text ? JSON.parse(text) : null;
  } else {
    responseData = await response.text();
  }

  if (!response.ok) {
    let errorMessage = "فشل الطلب";
    if (typeof responseData === "string" && responseData.trim()) {
      errorMessage = responseData;
    } else if (responseData && typeof responseData === "object") {
      if (typeof responseData.detail === "string") {
        errorMessage = responseData.detail;
      } else if (Array.isArray(responseData.detail)) {
        errorMessage = responseData.detail.map(item => item.msg).join(" | ");
      }
    }

    const error = new Error(errorMessage);
    error.status = response.status;
    throw error;
  }

  return responseData;
}