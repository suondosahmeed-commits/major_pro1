import json
import flet as ft


DATA_FILE = "users.json"


APP_NAME = "Soul Circle"
WELCOME_MESSAGE = "Welcome to Soul Circle, where true friendships begin!"


# Friendship / trust / helping colours
TRUST_GREEN = "#1C8A7A"
SOFT_MINT = "#EAF8F2"
LIGHT_GREEN = "#D5F1EA"
WHITE = "#FFFFFF"
DARK = "#1A3B36"
MUTED = "#496A63"
BORDER = "#CFE8E1"
HELP_GOLD = "#D9B843"


INPUT_TEXT = "#518f86"
CHOICE_TEXT = "#489a74"


AVATARS = ["🌼", "🌞", "🌳", "🦋", "🔈", "🐝", "🌙", "🌱", "🐟", "🦅", 
           "🌻", "🏀", "🔉", "🐴", "🦄", "🫎", "🐼", "🐫", "🐠", "🦆", 
           "🦢", "🐓", "🔊", "🏉", "🏐", "📚", "🥎"]


GENDERS = ["Female", "Male", "Non-binary", "Prefer not to say", "Other"]
PERSONALITIES = ["Introvert", "Extrovert", "Ambivert", "Omnivert"]
HOBBIES = [
    "Reading", "Gaming", "Music", "Art", "Movies",
    "Cooking", "Sports", "Travel", "Nature", "Photography",
    "Writing", "Dancing", "Chrocheting", "Yoga","Volunteering",
    "Board games", "Puzzles", "Gardening"
]
FRIENDSHIP_TYPES = ["Casual friendship", "Activity-based friendship", "Close friendship"]
COMMUNICATION = ["Texting", "Phone calls", "Video chat", "Face-to-face"]
ENERGY_LEVELS = ["Calm and quiet", "Balanced", "Very energetic"]
GROUPS = ["Small groups", "Large groups", "One-on-one", "Any of these"]
NEW_THINGS = ["Yes", "Sometimes", "Not usually"]
VALUES = [
        "Honesty", "Kindness", "Loyalty", "Respect",
        "Support", "Humour", "Good listener", "Deep conversations",
        "Empathy", "Trustworthiness", "Low maintenance"
]
ENVIRONMENT = ["Quiet space", "Busy social space", "Either is fine"]




# ==================
# Classes
# ==================

# This class for the user to log in
class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = password
        self.profile = {}


       
 # It converts the User object attributes into a standard Python dictionary for easy serialization.
    def to_dict(self):
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "profile": self.profile
        }




# this method reads and returns user records from the users.json data file, returning an empty list if the file is missing, invalid, or malformed.
class UserManager:
    def __init__(self):
        self.file_name = DATA_FILE


    # this method reads and returns user records from the users.json data file, returning an empty list if the file is missing, invalid, or malformed.
    def load_users(self):
        try:
            with open(self.file_name, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return []


        if type(data) == list:
            return data
        return []
   
   
    # It Writes the provided list of user dictionaries to the file with a four-space indentation format
    def save_users(self, users):
        with open(self.file_name, "w") as file:
            json.dump(users, file, indent=4)


    # Here, we search a list of user dictionaries for a matching username and returns the user data or None if not found.
    def find_user(self, users, username):
        for user in users:
            if user.get("username", "").lower() == username.lower():
                return user
        return None




# ==========================
# Helper functions
# ==========================


def hash_password(password):
    return password


# This method creates and styles a Flet dropdown menu element with a given label, list of selection choices, and an optional default value using custom theme colors.
def make_dropdown(label, choices, value=None):
    return ft.Dropdown(
        label=label,
        value=value,
        options=[ft.dropdown.Option(choice) for choice in choices],
        border_color=BORDER,
        focused_border_color=TRUST_GREEN,
        label_style=ft.TextStyle(color=DARK),
        text_style=ft.TextStyle(color=CHOICE_TEXT),
    )


# The "section_title" method generates a bold, 18-point header text element styled with the dark color scheme.
def section_title(text):
    return ft.Text(text, size=18, weight=ft.FontWeight.BOLD, color=DARK)


#The "primary_button" function builds a filled, rounded primary action button with custom padding, background color, and click handler support.
def primary_button(text_value, on_click, icon=None):
    return ft.Button(
        content=text_value,
        icon=icon,
        on_click=on_click,
        bgcolor=TRUST_GREEN,
        color=WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=ft.Padding(left=20, right=20, top=12, bottom=12),
        ),
    )


#This funcrtion builds an outlined secondary action button with a border and custom text styling matching the brand color palette.
def secondary_button(text_value, on_click):
    return ft.OutlinedButton(
        content=text_value,
        on_click=on_click,
        style=ft.ButtonStyle(
            color=TRUST_GREEN,
            side=ft.BorderSide(1, TRUST_GREEN),
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=ft.Padding(left=18, right=18, top=10, bottom=10),
        ),
    )




# card method is wraping a given content element inside a styled container card featuring a white background, padding, rounded corners, and a subtle border.
def card(content, width=None):
    return ft.Container(
        content=content,
        width=width,
        padding=20,
        bgcolor=WHITE,
        border=ft.Border.all(1, BORDER),
        border_radius=18,
    )




def compatibility_score(profile_a, profile_b):
    score = 0


    # Personality
    if profile_a.get("personality") == profile_b.get("personality"):
        score += 15
    elif "Ambivert" in (profile_a.get("personality"), profile_b.get("personality")):
        score += 8
    else:
        score += 4


    # Hobbies
    hobbies_a = set(profile_a.get("hobbies", []))
    hobbies_b = set(profile_b.get("hobbies", []))
    if hobbies_a or hobbies_b:
        overlap = len(hobbies_a & hobbies_b)
        total = len(hobbies_a | hobbies_b)
        score += round(20 * overlap / max(total, 1))


    # Friendship type
    if profile_a.get("friendship_type") == profile_b.get("friendship_type"):
        score += 12


    # Communication
    if profile_a.get("communication") == profile_b.get("communication"):
        score += 10


    # Values
    values_a = set(profile_a.get("values", []))
    values_b = set(profile_b.get("values", []))
    if values_a or values_b:
        overlap = len(values_a & values_b)
        total = len(values_a | values_b)
        score += round(15 * overlap / max(total, 1))


    # Energy level
    if profile_a.get("energy") == profile_b.get("energy"):
        score += 10


    # Group preference
    if profile_a.get("group_preference") == profile_b.get("group_preference"):
        score += 8


    # New experiences
    if profile_a.get("new_things") == profile_b.get("new_things"):
        score += 6
    else:
        score += 3


    # Environment
    if profile_a.get("environment") == profile_b.get("environment"):
        score += 6


    # Helping others
    if profile_a.get("helping_others") == profile_b.get("helping_others") == "Yes":
        score += 10


    return max(0, min(100, score))




def match_label(score):
    if score >= 85:
        return "Excellent potential"
    if score >= 70:
        return "Great match"
    if score >= 55:
        return "Good match"
    return "Possible friend"




def sort_by_score(item):
    return item[0]




def shared_count(profile_a, profile_b):
    count = 0


    if profile_a.get("personality") == profile_b.get("personality"):
        count += 1
    if profile_a.get("friendship_type") == profile_b.get("friendship_type"):
        count += 1
    if profile_a.get("communication") == profile_b.get("communication"):
        count += 1
    if profile_a.get("energy") == profile_b.get("energy"):
        count += 1
    if profile_a.get("group_preference") == profile_b.get("group_preference"):
        count += 1


    hobbies_a = set(profile_a.get("hobbies", []))
    hobbies_b = set(profile_b.get("hobbies", []))
    count += len(hobbies_a & hobbies_b)


    values_a = set(profile_a.get("values", []))
    values_b = set(profile_b.get("values", []))
    count += len(values_a & values_b)


    return count




# ================
# Main app
# ================


def main(page: ft.Page):
    page.title = APP_NAME
    page.bgcolor = ft.Colors.TRANSPARENT
   
    page.decoration = ft.BoxDecoration(
        image = ft.DecorationImage(
            src="bg4_cs.jpg",
            fit= ft.BoxFit.FILL,
        )
    )
    page.padding = 20
    page.window.width = 1000
    page.window.height = 820
    page.scroll = ft.ScrollMode.AUTO




    manager = UserManager()
    users = manager.load_users()
    current_username = None


    def refresh_users():
        nonlocal users
        users = manager.load_users()


    def find_user(username):
        return manager.find_user(users, username)


    def current_user():
        if current_username is None:
            return None
        return find_user(current_username)


    def set_page(content):
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Text("S", size=30, weight=ft.FontWeight.BOLD, color=WHITE),
                                    width=52,
                                    height=52,
                                    bgcolor=TRUST_GREEN,
                                    border_radius=14,
                                    alignment=ft.Alignment.CENTER,
                                ),
                                ft.Column(
                                    [
                                        ft.Text(APP_NAME, size=28, weight=ft.FontWeight.BOLD, color=DARK),
                                        ft.Text("Where true friendships begin", size=13, color=MUTED),
                                    ],
                                    spacing=0,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=12,
                        ),
                        ft.Container(height=8),
                        content,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                alignment=ft.Alignment(0.5, 0.5),
                padding=ft.Padding(left=0, right=0, top=12, bottom=30),
            )
        )
        page.update()


    # ----------------------
    # Welcome page
    # ----------------------
    def go_welcome(e=None):
        welcome_content = ft.Column(
            [
                ft.Text("🤝", size=52),
                ft.Text(
                    WELCOME_MESSAGE,
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=DARK,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Create a profile, answer friendship questions, and discover up to 100 friendly matches.",
                    size=16,
                    color=MUTED,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=10),
                primary_button("Get Started", go_register, icon=ft.Icons.ARROW_FORWARD),
                secondary_button("I already have an account", go_login),
                ft.Text("Real friendships grow from trust, kindness, and shared interests.", size=13, color=MUTED),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
            tight=True,
        )
        set_page(card(welcome_content, width=650))


    # -------------------------
    # Register page
    # -------------------------
    def go_register(e=None):
        username_field = ft.TextField(
            label="Choose a username",
            border_color=BORDER,
            focused_border_color=TRUST_GREEN,
            text_style=ft.TextStyle(color=INPUT_TEXT),
            label_style=ft.TextStyle(color=DARK),
        )
        password_field = ft.TextField(
            label="Create a password",
            password=True,
            can_reveal_password=True,
            border_color=BORDER,
            focused_border_color=TRUST_GREEN,
            text_style=ft.TextStyle(color=INPUT_TEXT),
            label_style=ft.TextStyle(color=DARK),
        )
        confirm_field = ft.TextField(
            label="Confirm password",
            password=True,
            can_reveal_password=True,
            border_color=BORDER,
            focused_border_color=TRUST_GREEN,
            text_style=ft.TextStyle(color=INPUT_TEXT),
            label_style=ft.TextStyle(color=DARK),
        )
        message = ft.Text("", color="red")


        def register_user(e):
            refresh_users()
            username = username_field.value.strip() if username_field.value else ""
            password = password_field.value or ""
            confirm = confirm_field.value or ""


            if len(username) < 3:
                message.value = "Username must be at least 3 characters."
            elif " " in username:
                message.value = "Username cannot contain spaces."
            elif find_user(username):
                message.value = "Username already exists."
            elif len(password) < 6:
                message.value = "Password must be at least 6 characters."
            elif password != confirm:
                message.value = "Passwords do not match."
            else:
                new_user = User(username, hash_password(password))
                users.append(new_user.to_dict())
                manager.save_users(users)


                nonlocal current_username
                current_username = username
                go_survey(first_time=True)
                return


            page.update()


        content = ft.Column(
            [
                section_title("Create your Soul Circle account"),
                username_field,
                password_field,
                confirm_field,
                message,
                primary_button("Create Account", register_user, icon=ft.Icons.PERSON_ADD_ALT_1),
                secondary_button("Back", go_welcome),
            ],
            spacing=14,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            tight=True,
        )
        set_page(card(content, width=520))


    # --------------------
    # Login page
    # --------------------
    def go_login(e=None):
        username_field = ft.TextField(
            label="Username",
            border_color=BORDER,
            focused_border_color=TRUST_GREEN,
            text_style=ft.TextStyle(color=INPUT_TEXT),
            label_style=ft.TextStyle(color=DARK),
        )
        password_field = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            border_color=BORDER,
            focused_border_color=TRUST_GREEN,
            text_style=ft.TextStyle(color=INPUT_TEXT),
            label_style=ft.TextStyle(color=DARK),
        )
        message = ft.Text("", color="red")


        def login_user(e):
            refresh_users()
            username = username_field.value.strip() if username_field.value else ""
            password = password_field.value or ""


            user = find_user(username)


            if not user or user.get("password_hash") != hash_password(password):
                message.value = "Incorrect username or password."
                page.update()
                return


            nonlocal current_username
            current_username = user["username"]


            if not user.get("profile"):
                go_survey(first_time=True)
            else:
                go_menu()


        content = ft.Column(
            [
                section_title("Welcome back"),
                username_field,
                password_field,
                message,
                primary_button("Log In", login_user, icon=ft.Icons.LOGIN),
                secondary_button("Create an account", go_register),
                secondary_button("Back", go_welcome),
            ],
            spacing=14,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            tight=True,
        )
        set_page(card(content, width=520))


    # ------------------------
    # Main menu
    # ------------------------
    def menu_tile(title, description, icon, on_click):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(icon, color=WHITE, size=26),
                        bgcolor=TRUST_GREEN,
                        width=50,
                        height=50,
                        border_radius=12,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column(
                        [
                            ft.Text(title, size=17, weight=ft.FontWeight.BOLD, color=DARK),
                            ft.Text(description, size=13, color=MUTED),
                        ],
                        spacing=3,
                        expand=True,
                    ),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=TRUST_GREEN),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=14,
            bgcolor=SOFT_MINT,
            border=ft.Border.all(1, BORDER),
            border_radius=14,
            on_click=on_click,
            ink=True,
        )


    def logout_action(e):
        nonlocal current_username
        current_username = None
        go_welcome()


    def go_menu(e=None):
        user = current_user()
        if not user:
            go_welcome()
            return


        first_name = user.get("profile", {}).get("first_name", user["username"])
        avatar = user.get("profile", {}).get("avatar", "🌿")


        content = ft.Column(
            [
                ft.Text(f"{avatar} Hello, {first_name}!", size=28, weight=ft.FontWeight.BOLD, color=DARK),
                ft.Text("Choose what you want to do next.", size=15, color=MUTED),
                ft.Container(height=6),
                menu_tile("My Profile", "Review your friendship profile.", ft.Icons.ACCOUNT_CIRCLE, go_profile),
                menu_tile("Update Survey", "Edit your answers and preferences.", ft.Icons.EDIT_NOTE, go_survey),
                menu_tile("Find Friends", "Find up to 100 friends in your circle.", ft.Icons.DIVERSITY_3, go_matches),
                ft.Container(height=8),
                secondary_button("Log Out", logout_action),
            ],
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            tight=True,
        )
        set_page(card(content, width=650))


    # ---------------------
    # Survey page
    # ---------------------
    def go_survey(e=None, first_time=False):
        user = current_user()
        if not user:
            go_login()
            return


        # the "user" word is a dictionary, profile is a key, returning an empty bracket
        old = user.get("profile", {})


        first_name = ft.TextField(
            label="First name",
            value=old.get("first_name", ""),
            border_color=BORDER,
            focused_border_color=TRUST_GREEN,
            text_style=ft.TextStyle(color=INPUT_TEXT),
            label_style=ft.TextStyle(color=DARK),
        )
        last_name = ft.TextField(
            label="Last name",
            value=old.get("last_name", ""),
            border_color=BORDER,
            focused_border_color=TRUST_GREEN,
            text_style=ft.TextStyle(color=INPUT_TEXT),
            label_style=ft.TextStyle(color=DARK),
        )
        age = ft.Dropdown(
            label="Age",
            value=str(old.get("age", "")) if old.get("age") else None,
            options=[ft.dropdown.Option(str(n)) for n in range(3, 101)],
            border_color=BORDER,
            focused_border_color=TRUST_GREEN,
            text_style=ft.TextStyle(color=CHOICE_TEXT),
            label_style=ft.TextStyle(color=DARK),
        )


        gender = make_dropdown("Gender", GENDERS, old.get("gender"))
        personality = make_dropdown("Personality", PERSONALITIES, old.get("personality"))
        friendship_type = make_dropdown("Friendship type", FRIENDSHIP_TYPES, old.get("friendship_type"))
        communication_type = make_dropdown("Best communication", COMMUNICATION, old.get("communication"))
        energy = make_dropdown("Energy level", ENERGY_LEVELS, old.get("energy"))
        group_preference = make_dropdown("Preferred group size", GROUPS, old.get("group_preference"))
        new_things = make_dropdown("Do you try new things?", NEW_THINGS, old.get("new_things"))
        environment_choice = make_dropdown("Preferred environment", ENVIRONMENT, old.get("environment"))
        helping_others = make_dropdown("Do you like helping others?", ["Yes", "Sometimes", "No"], old.get("helping_others"))
        avatar_choice = make_dropdown("Choose your avatar", AVATARS, old.get("avatar") or "🌿")


        old_hobbies = set(old.get("hobbies", []))
        hobby_checks = []
        for hobby in HOBBIES:
            hobby_checks.append(
                ft.Checkbox(
                    label=hobby,
                    value=hobby in old_hobbies,
                    active_color=TRUST_GREEN,
                    check_color=WHITE,
                    label_style=ft.TextStyle(color="#489a74"),
                )
            )


        old_values = set(old.get("values", []))
        value_checks = []
        for value in VALUES:
            value_checks.append(
                ft.Checkbox(
                    label=value,
                    value=value in old_values,
                    active_color=TRUST_GREEN,
                    check_color=WHITE,
                    label_style=ft.TextStyle(color="#489a74"),
                )
            )


        message = ft.Text("", color="red")


        def save_survey(e):
            if not first_name.value or not first_name.value.strip():
                message.value = "Please enter your first name."
            elif not last_name.value or not last_name.value.strip():
                message.value = "Please enter your last name."
            elif not age.value:
                message.value = "Please choose your age."
            elif not gender.value:
                message.value = "Please choose your gender."
            elif not personality.value:
                message.value = "Please choose your personality."
            elif not any(cb.value for cb in hobby_checks):
                message.value = "Please choose at least one hobby."
            elif not friendship_type.value:
                message.value = "Please choose your friend type."
            elif not communication_type.value:
                message.value = "Please choose your communication style."
            elif not energy.value:
                message.value = "Please choose your energy level."
            elif not group_preference.value:
                message.value = "Please choose your group preference."
            elif not new_things.value:
                message.value = "Please answer whether you try new things."
            elif not environment_choice.value:
                message.value = "Please choose your preferred environment."
            elif not helping_others.value:
                message.value = "Please answer whether you like helping others."
            elif not any(cb.value for cb in value_checks):
                message.value = "Please choose at least one value you want in a friend."
            else:
                profile = {
                    "first_name": first_name.value.strip(),
                    "last_name": last_name.value.strip(),
                    "age": int(age.value),
                    "gender": gender.value,
                    "personality": personality.value,
                    "hobbies": [cb.label for cb in hobby_checks if cb.value],
                    "friendship_type": friendship_type.value,
                    "communication": communication_type.value,
                    "energy": energy.value,
                    "group_preference": group_preference.value,
                    "new_things": new_things.value,
                    "environment": environment_choice.value,
                    "helping_others": helping_others.value,
                    "values": [cb.label for cb in value_checks if cb.value],
                    "avatar": avatar_choice.value or "🍃",
                }
                user["profile"] = profile
                manager.save_users(users)
                go_menu()
                return


            page.update()


        survey_content = ft.Column(
            [
                section_title("Friendship Survey"),
                ft.Text("Tell us about yourself so we can find friends who truly match your values.", color=MUTED),


                section_title("Choose your avatar"),
                avatar_choice,


                section_title("About you"),
                first_name,
                last_name,
                age,
                gender,
                personality,


                section_title("Hobbies"),
                ft.Container(
                    content=ft.Column(
                        [ft.Row(hobby_checks[i:i+3], spacing=10) for i in range(0, len(hobby_checks), 3)],
                        spacing=4,
                    ),
                    padding=12,
                    bgcolor=SOFT_MINT,
                    border_radius=12,
                ),


                section_title("Friendship preferences"),
                friendship_type,
                communication_type,
                energy,
                group_preference,
                new_things,
                environment_choice,
                helping_others,


                section_title("Values"),
                ft.Container(
                    content=ft.Column(
                        [ft.Row(value_checks[i:i+3], spacing=10) for i in range(0, len(value_checks), 3)],
                        spacing=4,
                    ),
                    padding=12,
                    bgcolor=SOFT_MINT,
                    border_radius=12,
                ),


                message,
                primary_button("Save Survey", save_survey, icon=ft.Icons.SAVE),
                secondary_button("Back to Menu", go_menu),
            ],
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            tight=True,
        )


        set_page(card(ft.Container(content=survey_content, width=760), width=780))


    # ----------------------
    # Profile page
    # ----------------------
    def go_profile(e=None):
        user = current_user()
        if not user or not user.get("profile"):
            go_survey()
            return


        p = user["profile"]
        avatar = p.get("avatar", "🌿")


        rows = [
            ("Name", f"{p.get('first_name', '')} {p.get('last_name', '')}"),
            ("Age", str(p.get("age", ""))),
            ("Gender", p.get("gender", "")),
            ("Personality", p.get("personality", "")),
            ("Hobbies", ", ".join(p.get("hobbies", []))),
            ("Friendship type", p.get("friendship_type", "")),
            ("Communication", p.get("communication", "")),
            ("Energy", p.get("energy", "")),
            ("Group preference", p.get("group_preference", "")),
            ("Values", ", ".join(p.get("values", []))),
            ("Likes helping others", p.get("helping_others", "")),
        ]


        profile_rows = [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(label, weight=ft.FontWeight.BOLD, color=DARK, width=170),
                        ft.Text(value or "Not set", color="#2D2D2D", expand=True),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                padding=10,
                border=ft.Border.only(bottom=ft.BorderSide(1, BORDER)),
            )
            for label, value in rows
        ]


        content = ft.Column(
            [
                ft.Text(f"{avatar}", size=52),
                section_title("My Profile"),
                ft.Text("This is the information used to generate your friendship matches.", color=MUTED),
                *profile_rows,
                primary_button("Edit Survey", go_survey, icon=ft.Icons.EDIT),
                secondary_button("Back to Menu", go_menu),
            ],
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            tight=True,
        )
        set_page(card(content, width=700))


    # -------------------------
    # Match page
    # -------------------------
    def go_matches(e=None):
        user = current_user()
        if not user or not user.get("profile"):
            go_survey()
            return


        refresh_users()
        mine = user["profile"]


        candidates = []
        for other in users:
            if other.get("username") == current_username:
                continue
            if not other.get("profile"):
                continue


            other_profile = other["profile"]
            score = compatibility_score(mine, other_profile)
            candidates.append((score, other))


        candidates.sort(key=sort_by_score, reverse=True)
        candidates = candidates[:100]


        match_cards = []
        if not candidates:
            match_cards.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.DIVERSITY_3, size=40, color=TRUST_GREEN),
                            ft.Text("No friends yet!", size=22, weight=ft.FontWeight.BOLD, color=DARK),
                            ft.Text("There are no other users with completed profiles yet.", color=MUTED, text_align=ft.TextAlign.CENTER),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=22,
                    bgcolor=SOFT_MINT,
                    border_radius=14,
                )
            )
        else:
            for score, other in candidates:
                p = other["profile"]
                avatar = p.get("avatar", "🛬🪻")


                mutual_count = shared_count(mine, p)
                shared_message = "6 things in common" if mutual_count >= 6 else f"{mutual_count} things in common"


                match_cards.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Column(
                                            [
                                                ft.Text(f"{avatar} {p.get('first_name', '')} {p.get('last_name', '')}".strip(), size=18, weight=ft.FontWeight.BOLD, color=DARK),
                                                ft.Text(f"Age {p.get('age', 'N/A')} • {p.get('personality', 'Unknown')}", size=13, color=MUTED),
                                            ],
                                            spacing=3,
                                            expand=True,
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text(f"{score}%", size=24, weight=ft.FontWeight.BOLD, color=TRUST_GREEN),
                                                ft.Text("match score", size=11, color=MUTED),
                                            ],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=0,
                                        ),
                                    ],
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.ProgressBar(value=score / 100, color=TRUST_GREEN, bgcolor=LIGHT_GREEN, height=8),
                                ft.Text(match_label(score), size=14, weight=ft.FontWeight.BOLD, color=DARK),
                                ft.Text(
                                    f"{shared_message} • Trust and kindness are both strong here.",
                                    size=13,
                                    color=MUTED,
                                ),
                            ],
                            spacing=10,
                        ),
                        padding=18,
                        bgcolor=WHITE,
                        border=ft.Border.all(1, BORDER),
                        border_radius=16,
                    )
                )


        content = ft.Column(
            [
                section_title("Your Friendship Matches"),
                ft.Text("Your results are based on shared interests, personality, trust, and kind values.", color=MUTED),
                *match_cards,
                primary_button("Refresh Matches", go_matches, icon=ft.Icons.REFRESH),
                secondary_button("Back to Menu", go_menu),
            ],
            spacing=14,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            tight=True,
        )
        set_page(card(ft.Container(content=content, width=700), width=760))

    go_welcome()




ft.run(main)



