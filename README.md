# Instructions on how to run the project

## 1. Dependencies

Make sure you have [docker](https://www.docker.com/) installed alongside with [docker compose](https://docs.docker.com/compose/).

## 2. Build and run the project

If you have the `make` command available you can simply:

```bash
$ make up
```

Or if you don't, execute these:

```bash
$ docker compose up --build
```

## 3. Test the endpoints

Now that the server is up and running, these are the endpoints that this API provides:

### First endpoint

```txt
POST http://localhost:8000/api/v1/coupons/
```

A payload for the first endpoint would look like this:

```jsonc
[
  // Request
  {
    "code": "coupon1",
    "type": "PERCENTAGE",
    "expiration_date": 1720729598, // An unix timestamp in seconds
    "max_redemption_quota": 3,
    "minimum_purchase_amount": 100.0,
    "discount_amount": 10,
    "first_purchase_only": false,
    "available_for_general_public": false
  },
  // Response
  {
    "code": "coupon1",
    "type": "PERCENTAGE",
    "expiration_date": 1720729598,
    "max_redemption_quota": 3,
    "minimum_purchase_amount": 100.0,
    "discount_amount": 10.0,
    "first_purchase_only": false,
    "available_for_general_public": false,
    "id": 1,
    "created_at": "2023-07-12T22:17:57.923883Z",
    "updated_at": "2023-07-12T22:17:57.923883Z"
  }
]
```

For the `type` prop, these are the possible enum values:

```txt
PERCENTAGE
FIXED_AMOUNT_GENERAL_PUBLIC
FIXED_AMOUNT_FIRST_PURCHASE
```

Also, there are some **validation rules**:

- The date set in the `expiration_date` field can not be lower than the current timestamp

- When the `type` is set to `FIXED_AMOUNT_FIRST_PURCHASE`, the value for the `first_purchase_only` field has to be true

- When the `type` is set to `FIXED_AMOUNT_GENERAL_PUBLIC`, the value for the `available_for_general_public` field has to be true

### Second endpoint

```txt
POST http://localhost:8000/api/v1/coupons/:coupon_code/
```

A payload for the second endpoint would look like this:

```jsonc
[
  // Request
  {
    "total_purchase_amount": 1000,
    "is_first_purchase": true
  },
  // Response
  {
    "total_purchase_amount": 1000.0,
    "is_first_purchase": true,
    "id": 1,
    "created_at": "2023-07-12T22:26:56.377452Z",
    "updated_at": "2023-07-12T22:26:56.377452Z",
    "total_amount_with_discount": 900.0,
    "coupon": {
      "code": "coupon1",
      "type": "PERCENTAGE",
      "expiration_date": 1720729598,
      "max_redemption_quota": 3,
      "minimum_purchase_amount": 100.0,
      "discount_amount": 10.0,
      "first_purchase_only": false,
      "available_for_general_public": false,
      "id": 1,
      "created_at": "2023-07-12T22:26:53.073318Z",
      "updated_at": "2023-07-12T22:26:53.073318Z"
    }
  }
]
```

Note that the `:coupon_code` path parameter is just the coupon code. Say you have a coupon named `coupon1`, then the url would look like this:

```txt
POST http://localhost:8000/api/v1/coupons/coupon1/
```

---

## Testing

The project has some tests implemented. To run them, you can do the following:

- If you have the `make` command available you can simply:

```bash
$ make test
```

- Or if you don't, execute these:

```bash
$ docker compose -f docker-compose-test.yaml up --build
$ docker rm coupon-codes-test-app
```
