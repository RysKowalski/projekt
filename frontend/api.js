export const API = (() => {
  let accessToken = null;

  /**
   * Authenticate and obtain an access token.
   */
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

    accessToken = data.access_token;

    return data;
  }

  /**
   * Clear the current access token.
   */
  function logout() {
    accessToken = null;
  }

  /**
   * Send an authenticated HTTP request.
   */
  async function request(url, options = {}) {
    if (!accessToken) {
      throw new Error("Not authenticated. Call login() first.");
    }

    const headers = new Headers(options.headers || {});

    headers.set("Authorization", `Bearer ${accessToken}`);

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

  /**
   * Convenience HTTP methods.
   */
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
