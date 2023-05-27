from st_pages import Page, add_page_title, show_pages

add_page_title("Portfolio Service")  # Optional method to add title and icon to current page

show_pages(
    [
        Page("pages/login_page.py", "Login Page", "🏠"),
        Page("pages/sign_in_page.py", "Sign in", "🧑"),
        Page("pages/find_password_page.py", "Find Password", "🔑"),
    ]
)

