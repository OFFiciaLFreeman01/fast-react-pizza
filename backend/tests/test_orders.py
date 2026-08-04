def _order_payload(pizza_id, priority=False, quantity=1):
    return {
        "customer": "Jane Doe",
        "phone": "1234567890",
        "address": "1 Main St",
        "priority": priority,
        "cart": [{"pizza_id": pizza_id, "quantity": quantity}],
    }


def test_create_order(client, sample_pizza):
    resp = client.post("/api/v1/order", json=_order_payload(sample_pizza.id, quantity=2))
    assert resp.status_code == 200
    data = resp.json()
    assert data["orderPrice"] == 24.0
    assert data["priorityPrice"] == 0
    assert data["status"] == "preparing"

    order_id = data["id"]
    resp = client.get(f"/api/v1/order/{order_id}")
    assert resp.status_code == 200
    assert resp.json()["customer"] == "Jane Doe"


def test_create_order_priority_adds_20_percent_fee(client, sample_pizza):
    resp = client.post("/api/v1/order", json=_order_payload(sample_pizza.id, priority=True))
    data = resp.json()
    assert data["priorityPrice"] == 2.4  # 20% of 12.00


def test_create_order_rejects_unknown_pizza(client):
    resp = client.post("/api/v1/order", json=_order_payload(999))
    assert resp.status_code == 400


def test_create_order_rejects_sold_out_pizza(client, sold_out_pizza):
    resp = client.post("/api/v1/order", json=_order_payload(sold_out_pizza.id))
    assert resp.status_code == 400
    assert "Sold out" in resp.json()["detail"]


def test_create_order_rejects_empty_cart(client, sample_pizza):
    payload = _order_payload(sample_pizza.id)
    payload["cart"] = []
    resp = client.post("/api/v1/order", json=payload)
    assert resp.status_code == 422


def test_create_order_rejects_invalid_phone(client, sample_pizza):
    payload = _order_payload(sample_pizza.id)
    payload["phone"] = "abc"
    resp = client.post("/api/v1/order", json=payload)
    assert resp.status_code == 422


def test_get_missing_order_returns_404(client):
    resp = client.get("/api/v1/order/doesnotexist")
    assert resp.status_code == 404


def test_toggle_priority_no_auth_required(client, sample_pizza):
    order_id = client.post("/api/v1/order", json=_order_payload(sample_pizza.id)).json()["id"]
    resp = client.patch(f"/api/v1/order/{order_id}", json={"priority": True})
    assert resp.status_code == 200
    assert resp.json()["priority"] is True
    assert resp.json()["priorityPrice"] == 2.4


def test_status_update_requires_auth(client, sample_pizza):
    order_id = client.post("/api/v1/order", json=_order_payload(sample_pizza.id)).json()["id"]
    resp = client.patch(f"/api/v1/order/{order_id}/status", json={"status": "out-for-delivery"})
    assert resp.status_code == 401


def test_status_update_with_valid_auth(client, sample_pizza, admin_token):
    order_id = client.post("/api/v1/order", json=_order_payload(sample_pizza.id)).json()["id"]
    resp = client.patch(
        f"/api/v1/order/{order_id}/status",
        json={"status": "out-for-delivery"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "out-for-delivery"


def test_status_update_rejects_skipping_a_step(client, sample_pizza, admin_token):
    order_id = client.post("/api/v1/order", json=_order_payload(sample_pizza.id)).json()["id"]
    resp = client.patch(
        f"/api/v1/order/{order_id}/status",
        json={"status": "delivered"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 400


def test_status_update_rejects_invalid_token(client, sample_pizza):
    order_id = client.post("/api/v1/order", json=_order_payload(sample_pizza.id)).json()["id"]
    resp = client.patch(
        f"/api/v1/order/{order_id}/status",
        json={"status": "out-for-delivery"},
        headers={"Authorization": "Bearer not-a-real-token"},
    )
    assert resp.status_code == 401


def test_list_orders_requires_auth(client, sample_pizza):
    client.post("/api/v1/order", json=_order_payload(sample_pizza.id))
    resp = client.get("/api/v1/order")
    assert resp.status_code == 401


def test_list_orders_with_auth(client, sample_pizza, admin_token):
    client.post("/api/v1/order", json=_order_payload(sample_pizza.id))
    client.post("/api/v1/order", json=_order_payload(sample_pizza.id))
    resp = client.get("/api/v1/order", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_list_orders_filters_by_status(client, sample_pizza, admin_token):
    order_id = client.post("/api/v1/order", json=_order_payload(sample_pizza.id)).json()["id"]
    client.post("/api/v1/order", json=_order_payload(sample_pizza.id))
    headers = {"Authorization": f"Bearer {admin_token}"}
    client.patch(
        f"/api/v1/order/{order_id}/status",
        json={"status": "out-for-delivery"},
        headers=headers,
    )

    resp = client.get("/api/v1/order?status=out-for-delivery", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["id"] == order_id
