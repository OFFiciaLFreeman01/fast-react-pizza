const API_URL = `${import.meta.env.VITE_API_URL ?? "http://localhost:8000"}/api/v1`;
const TOKEN_KEY = "kitchen_token";

export function getStoredToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function clearStoredToken() {
  localStorage.removeItem(TOKEN_KEY);
}

export async function login(username, password) {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw Error("Invalid username or password");

  const { access_token } = await res.json();
  localStorage.setItem(TOKEN_KEY, access_token);
  return access_token;
}

export async function getOrders(token, status) {
  const url = new URL(`${API_URL}/order`);
  if (status) url.searchParams.set("status", status);

  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (res.status === 401) throw Error("UNAUTHORIZED");
  if (!res.ok) throw Error("Failed loading orders");

  return await res.json();
}

export async function advanceOrderStatus(token, orderId, status) {
  const res = await fetch(`${API_URL}/order/${orderId}/status`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ status }),
  });
  if (res.status === 401) throw Error("UNAUTHORIZED");
  if (!res.ok) {
    const err = await res.json().catch(() => null);
    throw Error(err?.detail ?? "Failed updating order status");
  }
  return await res.json();
}
