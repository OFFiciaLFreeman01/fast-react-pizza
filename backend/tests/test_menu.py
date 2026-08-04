def test_menu_empty_when_no_pizzas(client):
    resp = client.get("/api/v1/menu")
    assert resp.status_code == 200
    assert resp.json() == []


def test_menu_returns_seeded_pizza(client, sample_pizza):
    resp = client.get("/api/v1/menu")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["name"] == "Margherita"
    assert data[0]["ingredients"] == ["tomato", "mozzarella", "basil"]
    assert data[0]["unit_price"] == 12.0
    assert data[0]["sold_out"] is False
