(function () {
  "use strict";

  const API_BASE = window.API_BASE_URL || "http://localhost:8000";
  const TOKEN_KEY = "oms_token";

  // ---------- tiny state ----------
  const state = {
    token: localStorage.getItem(TOKEN_KEY) || null,
    userId: null,
    userName: null,
    products: null, // cached list from GET /products
  };

  // ---------- dom refs ----------
  const authView = document.getElementById("auth-view");
  const appView = document.getElementById("app-view");

  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  const loginError = document.getElementById("login-error");
  const registerError = document.getElementById("register-error");
  const tabs = document.querySelectorAll(".ticket__tab");

  const accountNameEl = document.getElementById("account-name");
  const logoutBtn = document.getElementById("logout-btn");
  const navLinks = document.querySelectorAll(".app-nav__link");

  const catalogRoute = document.getElementById("catalog-route");
  const ledgerRoute = document.getElementById("ledger-route");
  const catalogGrid = document.getElementById("catalog-grid");
  const catalogStatus = document.getElementById("catalog-status");
  const ledgerList = document.getElementById("ledger-list");
  const ledgerStatus = document.getElementById("ledger-status");

  const toastEl = document.getElementById("toast");

  // ---------- helpers ----------
  function decodeJwtPayload(token) {
    try {
      const payload = token.split(".")[1];
      const json = atob(payload.replace(/-/g, "+").replace(/_/g, "/"));
      return JSON.parse(json);
    } catch (e) {
      return null;
    }
  }

  function showToast(message, isError) {
    toastEl.textContent = message;
    toastEl.hidden = false;
    toastEl.classList.toggle("is-error", !!isError);
    requestAnimationFrame(() => toastEl.classList.add("is-visible"));
    clearTimeout(showToast._t);
    showToast._t = setTimeout(() => {
      toastEl.classList.remove("is-visible");
      setTimeout(() => { toastEl.hidden = true; }, 200);
    }, 2600);
  }

  function money(n) {
    return Number(n).toLocaleString("en-IN");
  }

  function formatTimestamp(iso) {
    const d = new Date(iso);
    if (isNaN(d.getTime())) return iso;
    return d.toLocaleString("en-IN", {
      day: "2-digit", month: "short", year: "numeric",
      hour: "2-digit", minute: "2-digit",
    });
  }

  async function api(path, options = {}) {
    const headers = Object.assign(
      { "Content-Type": "application/json" },
      options.headers || {}
    );
    if (state.token) {
      headers["Authorization"] = "Bearer " + state.token;
    }
    const res = await fetch(API_BASE + path, Object.assign({}, options, { headers }));

    if (res.status === 401) {
      // token missing/expired/invalid — force back to sign-in
      logout("Your session expired. Please sign in again.");
      throw new Error("Unauthorized");
    }

    let body = null;
    const text = await res.text();
    if (text) {
      try { body = JSON.parse(text); } catch (e) { body = text; }
    }

    if (!res.ok) {
      const detail = (body && body.detail) ? body.detail : `Request failed (${res.status})`;
      throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
    }

    return body;
  }

  // ---------- auth ----------
  function setSession(token) {
    const payload = decodeJwtPayload(token);
    if (!payload || !payload.sub) {
      showToast("Received an invalid session token.", true);
      return false;
    }
    state.token = token;
    state.userId = Number(payload.sub);
    localStorage.setItem(TOKEN_KEY, token);
    return true;
  }

  function logout(message) {
    state.token = null;
    state.userId = null;
    state.userName = null;
    state.products = null;
    localStorage.removeItem(TOKEN_KEY);
    renderAuth();
    if (message) showToast(message, true);
  }

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => {
        t.classList.toggle("is-active", t === tab);
        t.setAttribute("aria-selected", t === tab ? "true" : "false");
      });
      const isLogin = tab.dataset.tab === "login";
      loginForm.hidden = !isLogin;
      registerForm.hidden = isLogin;
      loginError.hidden = true;
      registerError.hidden = true;
    });
  });

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    loginError.hidden = true;
    const fd = new FormData(loginForm);
    const submitBtn = loginForm.querySelector("button");
    submitBtn.disabled = true;
    try {
      const data = await api("/auth/login", {
        method: "POST",
        body: JSON.stringify({
          user_email: fd.get("user_email"),
          user_password: fd.get("user_password"),
        }),
      });
      if (setSession(data.access_token)) {
        await enterApp();
      }
    } catch (err) {
      loginError.textContent = err.message || "Could not sign in.";
      loginError.hidden = false;
    } finally {
      submitBtn.disabled = false;
    }
  });

  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    registerError.hidden = true;
    const fd = new FormData(registerForm);
    const submitBtn = registerForm.querySelector("button");
    submitBtn.disabled = true;
    try {
      await api("/user", {
        method: "POST",
        body: JSON.stringify({
          user_name: fd.get("user_name"),
          user_email: fd.get("user_email"),
          user_password: fd.get("user_password"),
        }),
      });
      // Auto sign-in right after opening the account.
      const data = await api("/auth/login", {
        method: "POST",
        body: JSON.stringify({
          user_email: fd.get("user_email"),
          user_password: fd.get("user_password"),
        }),
      });
      if (setSession(data.access_token)) {
        await enterApp();
      }
    } catch (err) {
      registerError.textContent = err.message || "Could not open an account.";
      registerError.hidden = false;
    } finally {
      submitBtn.disabled = false;
    }
  });

  logoutBtn.addEventListener("click", () => logout());

  // ---------- routing ----------
  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      window.location.hash = "#/" + link.dataset.route;
    });
  });

  function setActiveNav(route) {
    navLinks.forEach((l) => l.classList.toggle("is-active", l.dataset.route === route));
    catalogRoute.hidden = route !== "catalog";
    ledgerRoute.hidden = route !== "ledger";
  }

  function currentRoute() {
    const hash = window.location.hash.replace(/^#\/?/, "");
    return hash === "ledger" ? "ledger" : "catalog";
  }

  window.addEventListener("hashchange", () => {
    if (!state.token) return;
    const route = currentRoute();
    setActiveNav(route);
    if (route === "catalog") loadCatalog();
    else loadLedger();
  });

  // ---------- views ----------
  function renderAuth() {
    authView.hidden = false;
    appView.hidden = true;
    loginForm.reset();
    registerForm.reset();
  }

  async function enterApp() {
    authView.hidden = true;
    appView.hidden = false;
    accountNameEl.textContent = "";
    if (!window.location.hash) window.location.hash = "#/catalog";
    const route = currentRoute();
    setActiveNav(route);
    if (route === "catalog") await loadCatalog();
    else await loadLedger();
  }

  async function ensureProducts() {
    if (state.products) return state.products;
    const list = await api("/products");
    state.products = list;
    return list;
  }

  function productLookup() {
    const map = new Map();
    (state.products || []).forEach((p) => map.set(p.product_id, p));
    return map;
  }

  async function loadCatalog() {
    catalogStatus.hidden = true;
    catalogGrid.innerHTML = "";
    try {
      const products = await ensureProducts();
      if (!products.length) {
        catalogGrid.innerHTML = `<div class="empty-state">The counter is bare right now — nothing in stock.</div>`;
        return;
      }
      products.forEach((p) => catalogGrid.appendChild(renderProductCard(p)));
    } catch (err) {
      catalogStatus.textContent = err.message || "Could not load the catalog.";
      catalogStatus.hidden = false;
      catalogStatus.classList.add("is-error");
    }
  }

  function renderProductCard(product) {
    const card = document.createElement("article");
    card.className = "card";
    card.dataset.productId = product.product_id;

    card.innerHTML = `
      <span class="card__id">ITEM No. ${String(product.product_id).padStart(4, "0")}</span>
      <h3 class="card__name">${escapeHtml(product.product_name)}</h3>
      <p class="card__desc">${escapeHtml(product.description)}</p>
      <div class="card__footer">
        <span class="card__price">${money(product.price)}</span>
        <button class="order-btn" type="button">Place order</button>
      </div>
      <span class="stamp">ORDERED</span>
    `;

    const btn = card.querySelector(".order-btn");
    btn.addEventListener("click", () => placeOrder(product, card, btn));
    return card;
  }

  async function placeOrder(product, card, btn) {
    btn.disabled = true;
    btn.textContent = "Filing\u2026";
    try {
      await api(`/user/${state.userId}/orders`, {
        method: "POST",
        body: JSON.stringify({ product_id: product.product_id }),
      });
      card.classList.add("is-ordered");
      card.querySelector(".stamp").classList.add("is-visible");
      showToast(`Order filed for "${product.product_name}".`);
    } catch (err) {
      btn.disabled = false;
      btn.textContent = "Place order";
      showToast(err.message || "Could not place that order.", true);
    }
  }

  async function loadLedger() {
    ledgerStatus.hidden = true;
    ledgerList.innerHTML = "";
    try {
      await ensureProducts();
      const orders = await api(`/user/${state.userId}/orders`);
      if (!orders.length) {
        ledgerList.innerHTML = `<div class="empty-state">No orders filed yet. Head to the catalog to place your first one.</div>`;
        return;
      }
      const lookup = productLookup();
      orders
        .slice()
        .sort((a, b) => new Date(b.placed_at) - new Date(a.placed_at))
        .forEach((order) => ledgerList.appendChild(renderLedgerRow(order, lookup)));
    } catch (err) {
      ledgerStatus.textContent = err.message || "Could not load the dispatch log.";
      ledgerStatus.hidden = false;
      ledgerStatus.classList.add("is-error");
    }
  }

  function renderLedgerRow(order, lookup) {
    const row = document.createElement("div");
    row.className = "ledger-row";
    const product = lookup.get(order.product_id);
    const productName = product ? product.product_name : `Product #${order.product_id}`;

    row.innerHTML = `
      <span class="ledger-row__id">#${String(order.order_id).padStart(5, "0")}</span>
      <span class="ledger-row__product">${escapeHtml(productName)}</span>
      <span class="ledger-row__meta">${formatTimestamp(order.placed_at)}</span>
      <span class="ledger-row__status">${escapeHtml(order.status)}</span>
    `;
    return row;
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = String(str);
    return div.innerHTML;
  }

  // ---------- boot ----------
  (async function boot() {
    if (state.token) {
      const payload = decodeJwtPayload(state.token);
      const now = Math.floor(Date.now() / 1000);
      if (payload && payload.sub && payload.exp && payload.exp > now) {
        state.userId = Number(payload.sub);
        await enterApp();
        return;
      }
      localStorage.removeItem(TOKEN_KEY);
    }
    renderAuth();
  })();
})();
