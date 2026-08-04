import { useEffect, useState } from "react";
import {
  advanceOrderStatus,
  clearStoredToken,
  getOrders,
  getStoredToken,
  login,
} from "./apiKitchen";

const NEXT_STATUS = {
  preparing: "out-for-delivery",
  "out-for-delivery": "delivered",
};

const STATUS_LABEL = {
  preparing: "Preparing",
  "out-for-delivery": "Out for delivery",
  delivered: "Delivered",
};

function LoginForm({ onLoggedIn }) {
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      await login(username, password);
      onLoggedIn();
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="mx-auto mt-12 max-w-sm space-y-4 px-4">
      <h1 className="text-xl font-semibold">Kitchen sign in</h1>
      <input
        className="input w-full"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />
      <input
        className="input w-full"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      {error && <p className="text-sm text-red-600">{error}</p>}
      <button
        type="submit"
        disabled={isSubmitting}
        className="inline-block rounded-full bg-yellow-400 px-4 py-3 text-sm font-semibold uppercase tracking-wide text-stone-800 hover:bg-yellow-300 disabled:cursor-not-allowed disabled:opacity-70"
      >
        {isSubmitting ? "Signing in..." : "Sign in"}
      </button>
    </form>
  );
}

function OrdersDashboard({ onLoggedOut }) {
  const [orders, setOrders] = useState([]);
  const [statusFilter, setStatusFilter] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [busyOrderId, setBusyOrderId] = useState(null);

  async function loadOrders() {
    setIsLoading(true);
    setError(null);
    try {
      const token = getStoredToken();
      const data = await getOrders(token, statusFilter || undefined);
      setOrders(data);
    } catch (err) {
      if (err.message === "UNAUTHORIZED") {
        clearStoredToken();
        onLoggedOut();
        return;
      }
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    loadOrders();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusFilter]);

  async function handleAdvance(order) {
    const nextStatus = NEXT_STATUS[order.status];
    if (!nextStatus) return;
    setBusyOrderId(order.id);
    try {
      const token = getStoredToken();
      await advanceOrderStatus(token, order.id, nextStatus);
      await loadOrders();
    } catch (err) {
      if (err.message === "UNAUTHORIZED") {
        clearStoredToken();
        onLoggedOut();
        return;
      }
      setError(err.message);
    } finally {
      setBusyOrderId(null);
    }
  }

  function handleLogout() {
    clearStoredToken();
    onLoggedOut();
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-xl font-semibold">Kitchen dashboard</h1>
        <button onClick={handleLogout} className="text-sm text-stone-500 underline">
          Sign out
        </button>
      </div>

      <div className="mb-4 flex gap-2">
        {["", "preparing", "out-for-delivery", "delivered"].map((s) => (
          <button
            key={s || "all"}
            onClick={() => setStatusFilter(s)}
            className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wide ${
              statusFilter === s
                ? "bg-stone-800 text-stone-100"
                : "bg-stone-200 text-stone-600"
            }`}
          >
            {s ? STATUS_LABEL[s] : "All"}
          </button>
        ))}
      </div>

      {error && <p className="mb-4 text-sm text-red-600">{error}</p>}
      {isLoading && <p className="text-sm text-stone-500">Loading orders...</p>}

      {!isLoading && orders.length === 0 && (
        <p className="text-sm text-stone-500">No orders in this view.</p>
      )}

      <ul className="divide-y divide-stone-200">
        {orders.map((order) => (
          <li key={order.id} className="flex items-center justify-between gap-4 py-3">
            <div>
              <p className="font-semibold">
                #{order.id} &mdash; {order.customer}
                {order.priority && (
                  <span className="ml-2 rounded-full bg-red-500 px-2 py-0.5 text-xs uppercase text-red-50">
                    Priority
                  </span>
                )}
              </p>
              <p className="text-sm text-stone-500">
                {order.address} &middot; {order.items.length} item(s) &middot; $
                {(order.orderPrice + order.priorityPrice).toFixed(2)}
              </p>
            </div>

            <div className="flex items-center gap-3">
              <span className="text-sm font-medium text-stone-600">
                {STATUS_LABEL[order.status]}
              </span>
              {NEXT_STATUS[order.status] && (
                <button
                  onClick={() => handleAdvance(order)}
                  disabled={busyOrderId === order.id}
                  className="rounded-full bg-yellow-400 px-3 py-1.5 text-xs font-semibold uppercase tracking-wide text-stone-800 hover:bg-yellow-300 disabled:cursor-not-allowed disabled:opacity-70"
                >
                  {busyOrderId === order.id
                    ? "Updating..."
                    : `Mark ${STATUS_LABEL[NEXT_STATUS[order.status]]}`}
                </button>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

function Kitchen() {
  const [isAuthed, setIsAuthed] = useState(Boolean(getStoredToken()));

  if (!isAuthed) {
    return <LoginForm onLoggedIn={() => setIsAuthed(true)} />;
  }
  return <OrdersDashboard onLoggedOut={() => setIsAuthed(false)} />;
}

export default Kitchen;
