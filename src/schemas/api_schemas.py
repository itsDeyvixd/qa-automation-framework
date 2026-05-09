USER_OBJECT = {
    "type": "object",
    "required": ["id", "firstName", "lastName", "email", "username"],
    "properties": {
        "id":        {"type": "integer"},
        "firstName": {"type": "string", "minLength": 1},
        "lastName":  {"type": "string", "minLength": 1},
        "email":     {"type": "string"},
        "username":  {"type": "string", "minLength": 1},
    },
}
USER_LIST_RESPONSE = {
    "type": "object",
    "required": ["users", "total", "skip", "limit"],
    "properties": {
        "users": {"type": "array", "items": USER_OBJECT},
        "total": {"type": "integer"},
        "skip":  {"type": "integer"},
        "limit": {"type": "integer"},
    },
}
CREATE_USER_RESPONSE = {
    "type": "object",
    "required": ["id", "firstName", "lastName"],
    "properties": {
        "id": {"type": "integer"},
        "firstName": {"type": "string"},
        "lastName":  {"type": "string"},
    },
}
UPDATE_USER_RESPONSE = {
    "type": "object",
    "required": ["id"],
    "properties": {
        "id": {"type": "integer"},
        "firstName": {"type": "string"},
        "lastName":  {"type": "string"},
    },
}
DELETE_USER_RESPONSE = {
    "type": "object",
    "required": ["id", "isDeleted"],
    "properties": {
        "id":        {"type": "integer"},
        "isDeleted": {"type": "boolean"},
    },
}
LOGIN_SUCCESS_RESPONSE = {
    "type": "object",
    "required": ["accessToken", "refreshToken", "id", "username"],
    "properties": {
        "accessToken":  {"type": "string", "minLength": 1},
        "refreshToken": {"type": "string", "minLength": 1},
        "id":           {"type": "integer"},
        "username":     {"type": "string"},
        "email":        {"type": "string"},
        "firstName":    {"type": "string"},
        "lastName":     {"type": "string"},
    },
}
LOGIN_ERROR_RESPONSE = {
    "type": "object",
    "required": ["message"],
    "properties": {
        "message": {"type": "string", "minLength": 1},
    },
}
PRODUCT_OBJECT = {
    "type": "object",
    "required": ["id", "title", "price", "category"],
    "properties": {
        "id":       {"type": "integer"},
        "title":    {"type": "string", "minLength": 1},
        "price":    {"type": "number", "minimum": 0},
        "category": {"type": "string"},
        "stock":    {"type": "integer"},
        "rating":   {"type": "number"},
    },
}
PRODUCT_LIST_RESPONSE = {
    "type": "object",
    "required": ["products", "total", "skip", "limit"],
    "properties": {
        "products": {"type": "array", "items": PRODUCT_OBJECT},
        "total":    {"type": "integer"},
        "skip":     {"type": "integer"},
        "limit":    {"type": "integer"},
    },
}
