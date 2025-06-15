# 🧑‍💼 HR Management System – Task Assignment & Confirmation Portal

This is a FastAPI web application designed for managing employee tasks in an HR-like environment. It allows admin users to:

- View and manage users they have authority over.
- Assign tasks (with optional parent tasks).
- Confirm or reopen completed tasks.
- Track ongoing work in a user-friendly interface.

## 🚀 Features

- 👥 Role-based task delegation using `admin_rights` relationships.
- ✅ Confirmation mechanism for completed tasks.
- 🔗 Supabase as the backend for user and task data.
- 🧠 Intelligent parent-task linking (only self-assigned tasks allowed as parent).
- 📦 Lightweight and simple front-end using Jinja2 templates.

---

## 🧰 Technologies

- Python 3.9+
- FastAPI
- Jinja2
- Supabase (PostgREST API)
- Uvicorn
- bcrypt (for password hashing)

---

---

## ⚙️ Running Locally

1. **Clone the repository**:
    ```bash
    git clone https://github.com/YourUsername/HR_MS.git
    cd HR_MS
    ```

2. **Create virtual environment** *(optional but recommended)*:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file** and add your Supabase keys:
    ```
    SUPABASE_URL=https://yourproject.supabase.co
    SUPABASE_KEY=your-secret-api-key
    ```

5. **Run the server**:
    ```bash
    uvicorn main:app --reload
    ```

---

## 🌍 Deployment

You can deploy this on [Render](https://render.com), [Railway](https://railway.app), or even using Docker + VPS. Just make sure to keep your `.env` secret and set the correct environment variables in production.

---

## 🛡️ Security Notes

- **Do not commit your `.env`** file (use `.gitignore`).
- Always use hashed passwords (this app uses `bcrypt`).

---

## 🤝 Contributions

Pull requests are welcome. For major changes, open an issue first to discuss what you would like to change.

---

## 📄 License

MIT License.

