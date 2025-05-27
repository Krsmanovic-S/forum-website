# 🏋️‍♂️ Rep Talk

This is a fitness-focused forum web application designed for smooth interaction, content sharing, and community engagement. 

Built with Flask, PostgreSQL, and Bootstrap.

## 🚀 Website Features

### 🔐 Account System  

This implementation allows users to register, log in and customize their profiles. User data is stored securely in a **PostgreSQL Database** 
where their passwords are salted and hashed using **Werkzeug**.

Sign up forms have data validators implemented to make sure users provide the requested information correctly.

---

### 💬 Engagement Tools  

This is the bulk of the entire website, users can read posts, create them, comment on them and interact between one another with an upvote system. 

Posting and commenting is expanded with options to edit and delete as well as the option to reply to other people's comments.

---

### 🔍 3. Search Functionality  

Users can search posts that interest them by utilizing a search bar. This search function is implemented with **ElasticSearch**.

---

### 🗄️ 4. PostgreSQL Backend  

Backend built by **SQLAlchemy** using custom classes to store all relevant information needed by the website.

Tables utilize relationships between one another to support systems like upvotes and polls easily.

---

### 📱 5. Mobile Optimization  

Website is optimized for small, medium and large screens with added functionality for mobile devices.

Custom JavaScript allows for a responsive and dynamic sidebar on small devices as well as providing utilities on larger screens.

---

## 🛠 Tech Stack
- Python
- Flask
- PostgreSQL / SQLAlchemy
- Bootstrap 5
- Jinja2
- HTML / CSS / JavaScript

