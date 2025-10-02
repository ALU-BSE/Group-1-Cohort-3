# MoMo SMS API Documentation

## Users Endpoints

### List All Users

**Endpoint & Method:** GET /users

**Request Example:**
curl http://localhost:8000/users

**Response Example:**
```json
{
  "users": [
    {
      "id": "US_0001",
      "mobile_number": null
    },
    {
      "id": "US_0002",
      "mobile_number": null
    }
  ]
}
```

**Error Codes:**
`500 Internal Server Error` - Server error occurred

---

### Get User by ID

**Endpoint & Method:** `GET /users/{user_id}`

**Request Example:**
curl http://localhost:8000/users/US_0001

**Response Example:**
```json
{
  "id": "US_0001",
  "mobile_number": null
}
```

**Error Codes:**
- `404 Not Found` - User with specified ID does not exist
- `500 Internal Server Error` - Server error occurred

---

### Create New User

**Endpoint & Method:** `POST /users`

**Request Example:**
curl -X POST http://localhost:8000/users -H "Content-Type: application/json" -d '{"mobile_number": "+250788123456"}'

**Response Example:**
```json
{
  "id": "US_0013",
  "mobile_number": "+250788123456"
}
```

**Error Codes:**
- `400 Bad Request` - Invalid JSON format or invalid payload
- `500 Internal Server Error` - Server error occurred

---

### Update User

**Endpoint & Method:** `PUT /users/{user_id}`

**Request Example:**
curl -X PUT http://localhost:8000/users/US_0001 -H "Content-Type: application/json" -d '{"mobile_number": "+250788999888"}'

**Response Example:**
```json
{
  "id": "US_0001",
  "mobile_number": "+250788999888"
}
```

**Error Codes:**
- `400 Bad Request` - Invalid JSON format
- `404 Not Found` - User with specified ID does not exist
- `500 Internal Server Error` - Server error occurred

---

### Delete User

**Endpoint & Method:** `DELETE /users/{user_id}`

**Request Example:**
curl -X DELETE http://localhost:8000/users/US_0001

**Response Example:**
```json
{
  "deleted": "US_0001"
}
```

**Error Codes:**
- `404 Not Found` - User with specified ID does not exist
- `500 Internal Server Error` - Server error occurred

---

## Transactions Endpoints

### List All Transactions

**Endpoint & Method:** `GET /transactions`

**Request Example:**
curl http://localhost:8000/transactions

**Response Example:**
```json
{
  "transactions": [
    {
      "id": "SMS_0001",
      "protocol": 1,
      "address": "+250788123456",
      "date_sent": "2025-09-18T10:15:00Z",
      "type": 2,
      "subject": "Transaction Alert",
      "sms_body": "You have received 10,000 RWF from Alice Johnson.",
      "read": 1,
      "status": 0,
      "sub_id": "SUB101"
    }
  ]
}
```

**Error Codes:**
- `500 Internal Server Error` - Server error occurred

---

### Get Transaction by ID

**Endpoint & Method:** `GET /transactions/{transaction_id}`

**Request Example:**
curl http://localhost:8000/transactions/SMS_0001

**Response Example:**
```json
{
  "id": "SMS_0001",
  "protocol": 1,
  "address": "+250788123456",
  "date_sent": "2025-09-18T10:15:00Z",
  "type": 2,
  "subject": "Transaction Alert",
  "sms_body": "You have received 10,000 RWF from Alice Johnson.",
  "read": 1,
  "status": 0,
  "sub_id": "SUB101"
}
```

**Error Codes:**
- `404 Not Found` - Transaction with specified ID does not exist
- `500 Internal Server Error` - Server error occurred

---

### Create New Transaction

**Endpoint & Method:** `POST /transactions`

**Request Example:**
curl -X POST http://localhost:8000/transactions -H "Content-Type: application/json" -d '{"protocol": 1, "address": "+250788999888", "date_sent": "2025-10-02T14:30:00Z", "type": 2, "subject": "New Transaction", "sms_body": "You have sent 15,000 RWF to Bob Wilson.", "read": 0, "status": 0, "sub_id": "SUB103"}'

**Response Example:**
```json
{
  "id": "SMS_0003",
  "protocol": 1,
  "address": "+250788999888",
  "date_sent": "2025-10-02T14:30:00Z",
  "type": 2,
  "subject": "New Transaction",
  "sms_body": "You have sent 15,000 RWF to Bob Wilson.",
  "read": 0,
  "status": 0,
  "sub_id": "SUB103"
}
```

**Error Codes:**
- `400 Bad Request` - Invalid JSON format or invalid payload
- `500 Internal Server Error` - Server error occurred

---

### Update Transaction

**Endpoint & Method:** `PUT /transactions/{transaction_id}`

**Request Example:**
curl -X PUT http://localhost:8000/transactions/SMS_0001 -H "Content-Type: application/json" -d '{"read": 1, "status": 1, "sms_body": "You have received 10,000 RWF from Alice Johnson. Updated."}'

**Response Example:**
```json
{
  "id": "SMS_0001",
  "protocol": 1,
  "address": "+250788123456",
  "date_sent": "2025-09-18T10:15:00Z",
  "type": 2,
  "subject": "Transaction Alert",
  "sms_body": "You have received 10,000 RWF from Alice Johnson. Updated.",
  "read": 1,
  "status": 1,
  "sub_id": "SUB101"
}
```

**Error Codes:**
- `400 Bad Request` - Invalid JSON format
- `404 Not Found` - Transaction with specified ID does not exist
- `500 Internal Server Error` - Server error occurred

---

### Delete Transaction

**Endpoint & Method:** `DELETE /transactions/{transaction_id}`

**Request Example:**
curl -X DELETE http://localhost:8000/transactions/SMS_0001

**Response Example:**
```json
{
  "deleted": "SMS_0001"
}
```

**Error Codes:**
- `404 Not Found` - Transaction with specified ID does not exist
- `500 Internal Server Error` - Server error occurred
