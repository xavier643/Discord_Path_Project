// dev => '', so requests go to /auth,/me and the Vite proxy handles it
// prod => absolute URL from env
const API_BASE = import.meta.env.DEV ? "" : import.meta.env.VITE_API_BASE;

export async function apiGet(path) {
  const r = await fetch(`${API_BASE}${path}`, { credentials: "include" });
  return r;
}

export async function apiPost(path, body) {
  return fetch(`${API_BASE}${path}`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
}

export async function apiPatch(path, body) {
  return fetch(`${API_BASE}${path}`, {
    method: "PATCH",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
}

export async function apiDelete(path, body) {
  return fetch(`${API_BASE}${path}`, {
    method: "DELETE",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
}

export function loginWithDiscord() {
  window.location.href = `${API_BASE}/auth/discord/login`;
}

export async function logout() {
  try {
    await apiPost("/logout");
  } catch {
    console.error("failed to logout");
  }
  window.location.reload();
}
