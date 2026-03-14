/**
 * Agam API Client
 * Shared fetch helpers for all frontend pages.
 * Backend: http://localhost:8000
 */

const BASE_URL = "http://localhost:8000";

// --- Authentication Utilities ---
function getToken() {
    return localStorage.getItem("agam_token");
}

function getRole() {
    return localStorage.getItem("agam_role");
}

function setAuth(token, role) {
    localStorage.setItem("agam_token", token);
    localStorage.setItem("agam_role", role);
}

function logout() {
    localStorage.removeItem("agam_token");
    localStorage.removeItem("agam_role");
    window.location.href = "login.html";
}

function getAuthHeaders(isFormData = false) {
    const token = getToken();
    const headers = {};
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }
    // If we're sending JSON, add Content-Type. FormData automatically sets its own Content-Type.
    if (!isFormData) {
        headers["Content-Type"] = "application/json";
    }
    return headers;
}

/**
 * Register a new user.
 * @param {Object} userData - {username, email, password, role}
 */
async function register(userData) {
    const response = await fetch(`${BASE_URL}/auth/register`, {
        method: "POST",
        headers: getAuthHeaders(false),
        body: JSON.stringify(userData),
    });
    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || `Registration failed`);
    }
    return response.json();
}

/**
 * Login an existing user (OAuth2 form format).
 */
async function login(username, password) {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const response = await fetch(`${BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: formData,
    });
    if (!response.ok) {
        throw new Error(`Invalid credentials`);
    }
    return response.json();
}

/**
 * Upload an image file to the backend.
 * @param {File} file - The image File object from <input type="file">
 * @returns {Promise<{filename, image_url, analysis: {room, tags, quality}}>}
 */
async function uploadImage(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${BASE_URL}/upload/`, {
        method: "POST",
        headers: getAuthHeaders(true),
        body: formData,
    });

    if (!response.ok) {
        // If unauthorized, logout
        if (response.status === 401) logout();
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || `Upload failed: ${response.status}`);
    }

    return response.json();
}

/**
 * Search for properties using a natural language query.
 */
async function searchProperties(query = "", semantic = false) {
    const url = new URL(`${BASE_URL}/search/`);
    if (query.trim()) url.searchParams.set("q", query.trim());
    if (semantic) url.searchParams.set("semantic", "true");


    // Search might be public, but let's pass token if present
    const response = await fetch(url.toString(), {
        headers: getAuthHeaders(false)
    });
    if (!response.ok) {
        throw new Error(`Search failed: ${response.status}`);
    }
    return response.json();
}

/**
 * Fetch the full list of demo properties.
 */
async function getProperties() {
    const response = await fetch(`${BASE_URL}/properties/`, {
        headers: getAuthHeaders(false)
    });
    if (!response.ok) {
        throw new Error(`Failed to load properties: ${response.status}`);
    }
    return response.json();
}

/**
 * Check if the backend is reachable.
 */
async function pingBackend() {
    try {
        const res = await fetch(`${BASE_URL}/`, { signal: AbortSignal.timeout(3000) });
        return res.ok;
    } catch {
        return false;
    }
}
/**
 * Send a message to the Agam Intelligence chatbot.
 * @param {string} message - The user's message.
 * @param {string} language - The selected language.
 * @returns {Promise<{reply: string}>}
 */
async function sendChatMessage(message, language = "english") {
    const response = await fetch(`${BASE_URL}/chat/`, {
        method: "POST",
        headers: getAuthHeaders(false),
        body: JSON.stringify({ message, language }),
    });

    if (!response.ok) {
        throw new Error(`Chat failed: ${response.status}`);
    }
    return response.json();
}

/**
 * Get current user profile.
 */
async function getCurrentUser() {
    const response = await fetch(`${BASE_URL}/auth/me`, {
        headers: getAuthHeaders(false)
    });
    if (!response.ok) {
        if (response.status === 401) logout();
        throw new Error(`Session expired`);
    }
    return response.json();
}

/**
 * Create a new property.
 * @param {Object} propertyData - The property data to create.
 */
async function createProperty(propertyData) {
    const token = getToken();
    const resp = await fetch(`${BASE_URL}/properties/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(propertyData)
    });
    if (resp.status === 401) throw new Error("Session expired");
    if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err.detail || "Failed to create property");
    }
    return await resp.json();
}

async function loadProfile() {
    try {
        const user = await getCurrentUser();
        const initials = document.getElementById('userInitials');
        const name = document.getElementById('userName');
        const role = document.getElementById('userRole');
        const welcome = document.getElementById('welcomeName');

        if (initials) initials.textContent = user.username.substring(0, 2).toUpperCase();
        if (name) name.textContent = user.username;
        if (role) role.textContent = user.role;
        if (welcome) welcome.textContent = user.username;
        
        return user;
    } catch (err) {
        console.error("Profile load failed:", err);
        return null;
    }
}

// --- Admin Dashboard Helpers ---
async function getAdminStats() {
    const response = await fetch(`${BASE_URL}/admin/stats`, {
        headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error("Failed to fetch admin stats");
    return response.json();
}

async function getAdminUsers() {
    const response = await fetch(`${BASE_URL}/admin/users`, {
        headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error("Failed to fetch users");
    return response.json();
}

async function toggleUserStatus(userId) {
    const response = await fetch(`${BASE_URL}/admin/users/${userId}/status`, {
        method: 'POST',
        headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error("Failed to toggle user status");
    return response.json();
}

async function getModerationQueue() {
    const response = await fetch(`${BASE_URL}/admin/moderation`, {
        headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error("Failed to fetch moderation queue");
    return response.json();
}

async function processModeration(propId, action) {
    const response = await fetch(`${BASE_URL}/admin/moderation/${propId}/action?action=${action}`, {
        method: 'POST',
        headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error("Failed to process moderation");
    return response.json();
}
