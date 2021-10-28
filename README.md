# Installation

## with docker-compose

1) Clone project
```
git clone https://My_unique_name@bitbucket.org/My_unique_name/drf-poll.git
```

2) Build
```
docker-compose build
```
3) Run
```
docker-compose up -d
```
4) Check
```
http://127.0.0.1:8000/api/polls/
```
## without

1) Clone project
```
git clone https://My_unique_name@bitbucket.org/My_unique_name/drf-poll.git
```
2) Create local virtualenv
```
python3 -m venv venv
```
3) Install all requirements
```
pip install -r requirements.txt
```
4) Migrations
```
python3 manage.py makemigrations
python3 manage.py migrate
```
5) Load test data
```
python3 manage.py loaddata polls
```
6) Check
```
http://127.0.0.1:8000/api/polls/
```
# Polls API documentation


## Auth

#### Create JWT token for CRUD Polls, Questions, Options
### Request
```http
POST /auth/token/
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `username` | `string` | **Required** |
| `password` | `string` | **Required** |

### Response example
```javascript
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## Polls

### Create poll request

```http
POST /api/polls/ --header 'Authorization: Bearer <access token>'
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `title` | `string` | **max_length=300, required** |
| `description` | `text` | **Not required** |
| `start_at` | `date` | **Not required** |
| `finish_at` | `date` | **Not required**|

### Response example
```http
{
    "id": 3,
    "title": "test",
    "description": "test",
    "start_at": null,
    "finish_at": null
}
```

### Delete poll

```http
DELETE /api/polls/{poll_id}/ --header 'Authorization: Bearer <access token>'
```

### Update poll

```http
PUT /api/polls/{poll_id}/ --header 'Authorization: Bearer <access token>'
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `title` | `string` | **max_length=300, required** |
| `description` | `text` | **Not required** |
| `start_at` | `date` | **Not required** |
| `finish_at` | `date` | **Not required** |


## Question

### Create question request
```http
POST /api/questions/ --header 'Authorization: Bearer <access token>'
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `text` | `text` | **Required**. |
| `type` | `choice("one", "many", "text")` | **Required**. |
| `poll_id` | `integer` | **Required**. |

### Response example
```http
{
    "id": 4,
    "text": "test",
    "type": "text",
    "poll_id": 1
}
```
### Delete question

```http
DELETE /api/questions/{question_id}/ --header 'Authorization: Bearer <access token>'
```

### Update question

```http
PUT /api/questions/{question_id}/ --header 'Authorization: Bearer <access token>'
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `text` | `text` | **Required**. |
| `type` | `choice("one", "many", "text")` | **Required**. |
| `poll_id` | `integer` | **Required**. |


## Option

### Create option
```http
POST /api/options/ --header 'Authorization: Bearer <access token>'
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `text` | `text` | **Not required, default='Enter text'**. |
| `question_id` | `integer` | **Required** |

### Delete option

```http
DELETE /api/options/{option_id}/ --header 'Authorization: Bearer <access token>'
```

### Update option

```http
PUT /api/options/{option_id}/ --header 'Authorization: Bearer <access token>'
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `text` | `text` | **Not required, default='Enter text'**. |
| `question_id` | `integer` | **Required** |


## Answer

### Create answer
```http
POST /api/answers/ 
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `text_form` | `text` | **max_length=300, not required** |
| `question_id` | `integer` | **Required** |
| `poll_id` | `integer` | **Required** |
| `option_id` | `integer` | **Not required** |
| `user_id` | `integer` | **not required** |


### Response example
```http
{
    "id": 5,
    "user_id": null,
    "text_form": "...",
    "option": null,
    "question": {
        "id": 1,
        "text": "...",
        "type": "text",
        "poll_id": 1
    }
}
```

### Delete answer

```http
DELETE /api/answer/{answer_id}/
```

### Update answer

```http
PUT /api/answer/{answer_id}/
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `text_form` | `text` | **max_length=300, not required** |
| `question_id` | `integer` | **Required** |
| `poll_id` | `integer` | **Required** |
| `option_id` | `integer` | **Not required** |
| `user_id` | `integer` | **not required** |

## User answers

### Get list of all users answers in polls request
```http
GET /api/user/{user_id}/polls/
```
### Response example
```
[
    {
        "id": 1,
        "title": "...",
        "description": "...",
        "start_at": "2021-10-28T06:37:30Z",
        "finish_at": null,
        "answers": [
            {
                "id": 1,
                "user_id": 1,
                "text_form": "...",
                "option": null,
                "question": {
                    "id": 1,
                    "text": "...",
                    "type": "text",
                    "poll_id": 1
                }
            },
            ...
```

### Get all users answers in current poll
```http
GET /api/user/{user_id}/polls/{poll_id}/
```



