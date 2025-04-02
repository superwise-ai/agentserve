# API Reference

## Endpoints

### Health Check

```http
GET /health
```

Returns the health status of the server.

**Response**

```json
{
    "status": "ok"
}
```

### Agent Info

```http
GET /agent/info
```

Returns information about the deployed agent.

**Response**

```json
{
    "name": "string",
    "description": "string",
    "capabilities": ["string"],
    "version": "string"
}
```

### Synchronous Invoke

```http
POST /agent/invoke
```

Invokes the agent synchronously and returns the complete response.

**Request Body**

```json
{
    "question": "string",
    "context": "string",  // Optional
    "stream": false       // Must be false for sync requests
}
```

**Response**

```json
{
    "answer": "string",
    "metadata": {
        "key": "value"
    }
}
```

### Streaming Invoke

```http
POST /agent/invoke
```

Invokes the agent and streams the response as it's generated.

**Request Body**

```json
{
    "question": "string",
    "context": "string",  // Optional
    "stream": true        // Must be true for streaming
}
```

**Response**

Server-Sent Events (SSE) stream with JSON objects:

```json
{
    "content": "string",
    "metadata": {
        "key": "value"
    },
    "done": false
}
```

The final event will have `"done": true`.

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request

```json
{
    "detail": "Invalid request parameters"
}
```

### 500 Internal Server Error

```json
{
    "detail": "Internal server error occurred"
}
``` 