
const TOKEN_KEY = "access_token";

export const API = (() => {
  let accessToken = localStorage.getItem(TOKEN_KEY);

  function setToken(token) {
    accessToken = token;

    if (token) {
      localStorage.setItem(TOKEN_KEY, token);
    } else {
      localStorage.removeItem(TOKEN_KEY);
    }
  }

  async function login(username, password) {
    const response = await fetch("/api/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        username,
        password,
      }),
    });

    if (!response.ok) {
      throw new Error(`Login failed: ${response.status}`);
    }

    const data = await response.json();

    setToken(data.access_token);

    return data;
  }

  function logout() {
    setToken(null);
  }

  async function request(url, options = {}) {
    const token = localStorage.getItem(TOKEN_KEY);

    if (!token) {
      throw new Error("Not authenticated. Call login() first.");
    }

    accessToken = token;

    const headers = new Headers(options.headers || {});
    headers.set("Authorization", `Bearer ${token}`);

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      logout();
      throw new Error("Session expired. Please log in again.");
    }

    if (!response.ok) {
      throw new Error(`Request failed: ${response.status}`);
    }

    if (response.status === 204) {
      return null;
    }

    return response.json();
  }

  return {
    login,
    logout,
    request,

    get: (url, options = {}) =>
      request(url, { ...options, method: "GET" }),

    post: (url, body, options = {}) =>
      request(url, {
        ...options,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
        body: JSON.stringify(body),
      }),

    put: (url, body, options = {}) =>
      request(url, {
        ...options,
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
        body: JSON.stringify(body),
      }),

    delete: (url, options = {}) =>
      request(url, { ...options, method: "DELETE" }),
  };
})();
