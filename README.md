# 📰 React Blog Platform (Vite + React + TailwindCSS)

A responsive, full-stack blog publishing platform where users can browse, search, write, edit, and delete blog posts. Built using **React (Vite)** on the frontend and powered by a **FastAPI** backend.

## ✨ Features

1. 📝 **Create, Edit, and Delete Posts**  
   Users can write new blog posts, edit their existing ones, or delete them from their personal dashboard.

2. 👍 **Post Engagement**  
   Each post displays the total number of likes, views, and includes a comment section where users can write and view comments.

3. 📊 **User Profile Analytics**  
   The profile page shows:
   - Total likes and views across all posts.
   - Individual performance metrics for each post (likes, views, and comments).

4. 🔒 **Protected Routes with Authentication**  
   - Only logged-in users can:
     - Create a post
     - Like or comment on any post
     - Access the "My Posts" dashboard  
   - Unauthenticated users can only browse and read posts.
  
## 🛠️ Tech Stack

### 🧩 Frontend
- **React.js** – Component-based library for building the user interface
- **Tailwind CSS** – Utility-first CSS framework for responsive and clean styling
- **React Router DOM** – For routing between pages and implementing protected routes

### 🚀 Backend
- **FastAPI** – High-performance Python web framework for building RESTful APIs
- **OAuth2 with JOSE JWT** – Secure authentication system using JSON Web Tokens (JWT) for protected routes and user sessions

### 🗄️ Database
- **MongoDB** – NoSQL document database for storing posts, user data, and comments

## 🛠️ Getting Started

Follow these steps to run the project locally on your machine.

---

### 1. Clone the Repository

  ```bash
  git clone github.com/Pags2003/Blogging-Website
  cd Blogging-Website
  ```
### 2. Start the Backend

  a. Navigate to the backend folder:
  ```   
  bash
  cd Backend
  ```
  b. Install dependencies:
  ```
  bash
  pip install -r requirements.txt
  ```
  c. Run the FastAPI server using Uvicorn:
  ```
  bash
  uvicorn main:app --reload
  ```
  This will start the backend server at http://127.0.0.1:8000

### 3. Start the Frontend

  a. Open a new terminal and navigate to the frontend folder:
  ```
  bash
  cd Frontend/Blog
  ```
  b. Install dependencies:
  ```
  bash
  npm install
  ```
  c. Run the React development server:
  ```
  bash
  npm run dev
  ```
  This will start the frontend at http://localhost:5173 (or a similar port

## 📁 Project Structure

The project is divided into two main parts: `frontend` and `backend`.

---

### 🖥️ Frontend (React)

Located in the `frontend/` folder. Built using **React.js** with **Tailwind CSS** and **React Router DOM** for styling and routing.

#### Main Files:

- `src/`
  - `App.jsx` – Main application component with routing setup
  - `components/`
    - `Navbar.jsx` – Navigation bar across the app
    - `PostCard.jsx` – UI card for displaying a single post
    - `PostsList.jsx` – Renders a list of posts
    - `PrivateRoute.jsx` – Handles route protection for authenticated users
    - `SearchBar.jsx` – Search input for filtering posts
  - `pages/`
    - `CreatePost.jsx` – Page to create a new blog post
    - `EditPost.jsx` – Page to edit an existing post
    - `Home.jsx` – Home page listing all blog posts
    - `Login.jsx` – User login page
    - `MyPosts.jsx` – Shows posts created by the logged-in user
    - `PostDetails.jsx` – Detailed view of a single post with comments, likes, and views
    - `ProfilePage.jsx` – User profile page showing stats like total likes and views
    - `Signup.jsx` – User signup/registration page

---

### ⚙️ Backend (FastAPI + MongoDB)

Located in the `backend/` folder. Built using **FastAPI**, with **OAuth2 JOSE JWT** for authentication and **Mongoose** (via `motor` or `beanie`) for MongoDB.

#### Folder Structure:

- `auth/` – Handles authentication logic (login, signup, token creation, validation)
- `config/` – Environment configuration and database setup
- `models/` – MongoDB data models (e.g., User, Post, Comment)
- `routes/` – API route handlers (e.g., `/posts`, `/auth`)
- `schemas/` – Pydantic schemas for request/response validation

#### Root File:

- `main.py` – Entry point for the FastAPI app

## 👨‍💻 Author

**Pratham Golhani**  
🌐 Portfolio: [prathamgolhani.netlify.app](https://prathamgolhani.netlify.app)
