# Core Features & API Design

This document provides details about the Core Feature and API endpoints available in the User Management System.
### 1. Core Features & API Design

#### Essential Functionalities

##### User Management:
- Create, update, delete, and retrieve user accounts.
- Enable/disable user accounts.

##### Role Management:
- Assign roles to users.
- Create, update, delete roles.

##### Permission Management:
- Define permissions and assign them to roles.
- Check if a user has specific permissions.

##### Authentication & Authorization:
- User registration and login.
- Token-based authentication (JWT/OAuth2).
- Password reset and recovery.

##### Logging & Auditing:
- Track user login attempts.
- Log administrative changes to roles and permissions.
## Base URL
```
http://localhost/api/
```

---

## **User Management**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/users/` | Create a new user |
| `GET`  | `/users/{id}/` | Retrieve user details |
| `PUT`  | `/users/{id}/` | Update user information |
| `DELETE` | `/users/{id}/` | Delete a user |

### **Example Request**
#### **Create a User**
```http
POST /api/users/
Content-Type: application/json
```
```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "securepassword"
}
```

### **Example Response**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "johndoe",
  "email": "johndoe@example.com",
  "is_active": true,
  "created_at": "2025-03-05T12:34:56Z"
}
```

---

## **Role Management**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/roles/` | Create a role |
| `GET`  | `/roles/{id}/` | Retrieve role details |
| `PUT`  | `/roles/{id}/` | Update a role |
| `DELETE` | `/roles/{id}/` | Delete a role |
| `POST` | `/roles/assign/` | Assign a role to a user |

---

## **Permission Management**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/permissions/` | Define a permission |
| `GET`  | `/permissions/{id}/` | Retrieve permission details |
| `PUT`  | `/permissions/{id}/` | Update a permission |
| `DELETE` | `/permissions/{id}/` | Delete a permission |
| `GET`  | `/users/{id}/permissions/` | Check user permissions |

---

## **Authentication & Authorization**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/auth/register/` | Register a new user |
| `POST` | `/auth/login/` | Authenticate a user and return a token |
| `POST` | `/auth/logout/` | Log out the user |
| `POST` | `/auth/password-reset/` | Initiate password reset |
| `POST` | `/auth/password-reset/confirm/` | Confirm password reset |

---

## **Logging & Auditing**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/logs/` | Retrieve system logs |

---

### **Authentication**
Most endpoints require an authentication token. You need to include an `Authorization` header in requests:

```http
Authorization: Bearer <your_token>
```

---


## **Tables and Relationships**

### **Users Table**
- `id` (Primary Key, UUID)
- `username` (Unique, String)
- `email` (Unique, String)
- `password_hash` (String)
- `is_active` (Boolean, Default: True)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### **Roles Table**
- `id` (Primary Key, UUID)
- `name` (Unique, String)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### **Permissions Table**
- `id` (Primary Key, UUID)
- `name` (Unique, String)
- `description` (String)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### **User_Roles Table (Many-to-Many Relationship)**
- `id` (Primary Key, UUID)
- `user_id` (Foreign Key -> Users)
- `role_id` (Foreign Key -> Roles)

### **Role_Permissions Table (Many-to-Many Relationship)**
- `id` (Primary Key, UUID)
- `role_id` (Foreign Key -> Roles)
- `permission_id` (Foreign Key -> Permissions)

---


## **Database Schema**
```sql
CREATE TABLE Users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE User_Roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    role_id UUID NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES Roles(id) ON DELETE CASCADE,
    UNIQUE (user_id, role_id)
);

CREATE TABLE Role_Permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id UUID NOT NULL,
    permission_id UUID NOT NULL,
    FOREIGN KEY (role_id) REFERENCES Roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES Permissions(id) ON DELETE CASCADE,
    UNIQUE (role_id, permission_id)
);
```


## **Performance Optimizations**
- **Database Indexing:** Apply indexes to frequently queried fields.
- **Caching with Redis:** Cache frequently accessed queries and authentication tokens.
- **Gunicorn Optimization:** Increase worker threads to handle concurrent requests.



