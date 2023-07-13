from httpx import AsyncClient


async def test_register_coupon(create_coupon_data: dict, client: AsyncClient) -> None:
    endpoint = "/api/v1/coupons/"

    response = await client.post(url=endpoint, json=create_coupon_data)
    response_data = tuple(response.json().items())

    assert response.status_code == 201
    assert ("id", 1) in response_data

    response = await client.post(url=endpoint, json=create_coupon_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "The code provided is registered in the database already"}


async def test_consume_coupon(
    create_coupon_data: dict, consume_coupon_data: dict, client: AsyncClient
) -> None:
    create_coupon_data["code"] = "coupon2"

    await client.post(url="/api/v1/coupons/", json=create_coupon_data)

    endpoint = f"/api/v1/coupons/{create_coupon_data['code']}/"
    response = await client.post(url=endpoint, json=consume_coupon_data)
    response_data = tuple(response.json().items())

    assert response.status_code == 200
    assert ("id", 1) in response_data

    endpoint = f"/api/v1/coupons/random/"
    response = await client.post(url=endpoint, json=consume_coupon_data)

    assert response.status_code == 404
    assert response.json() == {"detail": f"Coupon {'random'!r} not found"}
