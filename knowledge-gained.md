bacause I came from a nodejs background, i kept asking questions regarding olders like models, controllers, routes, etc, and i learned that FastAPI is designed differently, so I have to stop thinking in terms of traditional MVC (Model-View-Controller).

The Directory Structure I learnt about:

- core/: This is where my application's global configuration lives. i use core/ to validate your .env variables so that if a database password is missing, the API crashes immediately on startup, not halfway through a user's request.
- models/: In Python web development, "models" usually refers to ORM classes (like SQLAlchemy). Because i am writing raw SQL to maximize performance, i do not have ORM models. i only have database tables (which exist in Postgres) and `schemas/` (Pydantic classes that validate the JSON data coming in and going out).
- controllers/ and routes/: We use the api/ folder for our routes (endpoints). The actual logic that talks to the database will live in your `db/` folder. This keeps your endpoints clean and your database logic separate.

# asyncpg and a Connection Pool?

> Briefly explain what a connection pool is, focusing on the key concepts I need to understand it properly.

To connect Python to PostgreSQL, you need a driver (a specialized software program that acts as a translator between your computer's operating system and a hardware device.). asyncpg is an asynchronous driver. It is incredibly fast because it is non-blocking. When your API asks the database for a note, it does not freeze and wait. It handles other users' requests while the database does its job.

A connection pool is exactly what it sounds like. Opening a new database connection over the network takes time and memory. If 1,000 users hit your API at the same time, opening 1,000 new connections will crash your database. A pool keeps a small batch of connections open permanently (for example, 10 connections). When a user makes a request, the API borrows one connection, runs the SQL query, and hands the connection back to the pool. It is highly efficient.

---

In other words, a connection pool is a cache of active database connections maintained in memory by your application backend. Instead of opening a brand-new connection to your relational database (like PostgreSQL or MySQL) every single time an API request arrives, FastAPI borrows an existing, open connection from the pool, runs the query, and instantly returns it to the pool when finished.

---

A connection pool is a collection of already-created database connections that your application can reuse instead of creating a new connection every time it needs to talk to the database.

Think of it like a parking lot of database connections:

1. Your app needs the database → take an available connection from the pool.
2. Run your query → SELECT, INSERT, etc.
3. Finish → return the connection to the pool.
4. Another request can reuse it.

The key things to understand

Connection ≠ query
A connection is the communication channel between your application and the database. A query is something you send through that channel.

The pool has a limit
For example, you might configure 10 connections. If 10 are being used, an 11th request has to wait for one to become available.

It improves performance ⚡
Creating a database connection can be expensive. Reusing existing connections avoids repeatedly doing that setup.

It controls database load
Without a pool, hundreds of incoming requests could potentially create hundreds of database connections and overwhelm the database.

Connections are reused, not permanently owned by one request
Request A can use connection #3, return it, and request B can later use that same connection.


The mental model to remember:

> Connection pool = a limited set of reusable database connections shared by your application.

For backend development, the big idea is: borrow → use → release → reuse.

---

> Who actually creates the connections in a connection pool? Do I manually create them in code, or does the pool automatically create and cache multiple database connections?

Exactly. You normally do not manually create 10 connections yourself.

The database driver or connection-pool library does it for you.

For example, in a Node.js/PostgreSQL application, you might write something conceptually like:

const pool = new Pool({
  max: 10
});

You are basically telling the pool:

> "Manage up to 10 database connections for my application."

Then the pool handles the rest.

What actually happens?

Imagine your app starts:

Your Application
       │
       ▼
 Connection Pool
 ┌─────┬─────┬─────┬─────┐
 │ C1  │ C2  │ C3  │ ... │  ← connections created/managed by pool
 └─────┴─────┴─────┴─────┘
       │
       ▼
    Database

The pool may create connections as they are needed, depending on the library/configuration.

When a request comes in:

Request 1 → borrow C1 → query → return C1
Request 2 → borrow C1 → query → return C1
Request 3 → borrow C2 → query → return C2

So no, you don't connect to the database 10 times and then somehow cache those connections yourself.

The pool manages the connections and keeps reusable connections available.

One important distinction

The connections aren't "cached queries" or cached data.

They're live communication channels to the database.

Think:

> Pool = manager
Connections = workers
Queries = jobs

The manager gives an available worker a job, the worker does it, then becomes available for the next job.

That's the core idea.

---

# My PostgreSQL database URL

To find your PostgreSQL database URL (also known as a connection string or URI), you can either assemble it yourself from your connection details or copy it directly from your hosting provider's dashboard.

## 1. Construct It Manually

If you are running PostgreSQL locally or have standard credentials, you can construct the URL using this standard format:

```
postgresql://username:password@host:port/database_name
```

To find these specific components:
- Protocol: Always postgresql:// (or postgres://). 
- Username: The default is usually postgres.
- Password: The password you set during installation or user creation. (Note: If your password contains special characters like @, #, or :, they must be percent-encoded).
- Host: localhost or 127.0.0.1 for local databases, or an IP/domain for remote ones.
- Port: The standard PostgreSQL port is 5432.
- Database Name: The specific database you want to connect to (e.g., mydb).

Example local URL: `postgresql://postgres:secret123@localhost:5432/my_app_db`

## 2. Find It in Common Environments

If you aren't sure of your credentials, use the method below that matches your setup:

**From the Terminal (psql)**

If you are already logged into the database via the terminal, run this command:

```
\conninfo
```

This will print your current user, port, and database.

---

# `Import block is un-sorted or un-formatted` Error

ruff handles import sorting (isort rules) automatically and will reformat your import block to comply with standard formatting rules.

If you want ruff to automatically fix imports on every save, add it to your project dependencies:

```bash
uv add --dev ruff
```

Then sort and format your entire codebase with:

```bash
uv run ruff check --fix .
uv run ruff format .
```

* `ruff check` handles linting (finding code bugs and sorting imports)
* `ruff format` handles code formatting (spacing, line lengths, and quotes)

---

# BaseModel vs BaseSettings

BaseModel is designed for data validation and serialization of request or response bodies, while BaseSettings is specialized for application configuration and automatically loads values from external sources like environment variables.
