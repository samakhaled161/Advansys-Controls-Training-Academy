import streamlit as st
import re
from supabase import create_client


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Advansys ESC | Controls Training Academy",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# SUPABASE
# =========================================================

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)


# =========================================================
# VALID PAGES
# =========================================================

VALID_PAGES = {
    "home",
    "register",
    "login",
    "choose_team",
    "teams",
    "dashboard",
}


# =========================================================
# SESSION STATE
# =========================================================

if "selected_team" not in st.session_state:
    st.session_state.selected_team = "PF"

if "completed_modules" not in st.session_state:
    st.session_state.completed_modules = []

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None


# =========================================================
# URL ROUTING
# =========================================================

def get_page_from_url():

    page = st.query_params.get("page", "home")

    if page not in VALID_PAGES:
        page = "home"

    return page


current_page = get_page_from_url()


def go_to(page):

    if page not in VALID_PAGES:
        page = "home"

    st.query_params["page"] = page


def select_team(team):

    st.session_state.selected_team = team
    go_to("dashboard")


# =========================================================
# COMPANY EMAIL VALIDATION
# =========================================================

def is_valid_company_email(email):

    pattern = r"^[A-Za-z]+\.[A-Za-z]+@advansys-esc\.com$"

    return re.fullmatch(pattern, email) is not None


# =========================================================
# AUTH FUNCTIONS
# =========================================================

def register_user(email, password):

    try:

        response = supabase.auth.sign_up(
            {
                "email": email,
                "password": password,
            }
        )

        if response.user is not None:

            st.session_state.current_user = email

            go_to("login")

            return True

        return False

    except Exception as e:

        error_message = str(e).lower()

        if (
            "already registered" in error_message
            or "already exists" in error_message
            or "user already registered" in error_message
        ):

            st.error(
                "This account is already registered."
            )

        else:

            st.error(
                "Registration failed. Please try again."
            )

        return False


def login_user(email, password):

    try:

        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )

        if response.user is not None:

            st.session_state.logged_in = True
            st.session_state.current_user = email

            go_to("choose_team")

            return True

        return False

    except Exception:

        return False


# =========================================================
# TEAM DATA
# =========================================================

teams = {

    "PF": {
        "name": "PF Team",
        "full_name": "Pallet Flow",
        "description": "Training resources and technical references for the PF team.",
        "icon": "📦",
        "topics": [
            "Pallet conveyor systems",
            "Power and device bus",
            "Hardware design documentation",
            "Controls and field devices",
        ],
    },

    "FLEX": {
        "name": "FLEX Team",
        "full_name": "Flexible Automation",
        "description": "Technical learning resources for flexible automation projects.",
        "icon": "🔄",
        "topics": [
            "Conveyor and material handling",
            "Electrical hardware design",
            "PLC fundamentals",
            "System integration",
        ],
    },

    "EMEA": {
        "name": "EMEA Team",
        "full_name": "Europe, Middle East & Africa",
        "description": "Shared learning materials and engineering references for EMEA projects.",
        "icon": "🌍",
        "topics": [
            "Project documentation",
            "Hardware standards",
            "Controls engineering",
            "Testing and commissioning",
        ],
    },

    "AMZ": {
        "name": "AMZ Team",
        "full_name": "Amazon Projects",
        "description": "Learning resources for automation systems in Amazon projects.",
        "icon": "🏭",
        "topics": [
            "Warehouse automation",
            "Conveyor and sorting",
            "Electrical design",
            "Controls integration",
        ],
    },
}


# =========================================================
# TRAINING CONTENT
# =========================================================

modules = [

    {
        "title": "Company Introduction",
        "category": "Getting Started",
        "description": "Learn about Advansys ESC, the academy, and the engineering teams.",
        "duration": "15 min",
    },

    {
        "title": "Warehouse Automation Fundamentals",
        "category": "Fundamentals",
        "description": "Understand material handling, conveyor systems, and sorting solutions.",
        "duration": "30 min",
    },

    {
        "title": "Hardware & Installation",
        "category": "Hardware Design",
        "description": "Explore electrical drawings, power distribution, and device connections.",
        "duration": "45 min",
    },

    {
        "title": "Controls & PLC Fundamentals",
        "category": "Controls",
        "description": "Get introduced to PLCs, control logic, and system interfaces.",
        "duration": "40 min",
    },

]


# =========================================================
# CUSTOM CSS
# =========================================================

st.html(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #f5f7fa;
        color: #182230;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .block-container {
        max-width: 1220px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }

    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 22px;
        background: #ffffff;
        border: 1px solid #e7ebf0;
        border-radius: 14px;
        margin-bottom: 28px;
        box-shadow: 0 4px 16px rgba(20, 35, 55, 0.04);
    }

    .logo-text {
        font-size: 23px;
        font-weight: 900;
        letter-spacing: 1px;
        color: #142334;
    }

    .logo-green {
        color: #7dbb43;
    }

    .academy-name {
        color: #526173;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-top: 2px;
    }

    .topbar-tag {
        font-size: 12px;
        font-weight: 700;
        color: #526173;
        background: #f1f5f8;
        border-radius: 20px;
        padding: 9px 14px;
    }

    .hero {
        background: linear-gradient(120deg, #102338 0%, #173a50 65%, #245a59 100%);
        border-radius: 22px;
        padding: 58px 54px;
        color: white;
        position: relative;
        overflow: hidden;
        margin-bottom: 30px;
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 330px;
        height: 330px;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 50%;
        right: -70px;
        top: -90px;
        box-shadow: 0 0 0 35px rgba(255,255,255,0.025),
                    0 0 0 75px rgba(255,255,255,0.02);
    }

    .hero-small {
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 3px;
        color: #a7d66b;
        margin-bottom: 16px;
    }

    .hero-title {
        font-size: clamp(34px, 5vw, 58px);
        font-weight: 900;
        line-height: 1.08;
        letter-spacing: -1.5px;
        margin-bottom: 16px;
        max-width: 760px;
    }

    .hero-title span {
        color: #a7d66b;
    }

    .hero-description {
        font-size: 16px;
        line-height: 1.8;
        color: #d8e2e9;
        max-width: 650px;
        margin-bottom: 26px;
    }

    .hero-pill {
        display: inline-block;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 30px;
        padding: 10px 16px;
        font-size: 12px;
        font-weight: 700;
        color: #f4f8fb;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    .section-kicker {
        color: #6a9e36;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2.2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .section-title {
        font-size: 28px;
        line-height: 1.25;
        font-weight: 850;
        color: #182b3d;
        margin: 0 0 12px 0;
    }

    .section-description {
        font-size: 14px;
        line-height: 1.8;
        color: #667587;
        margin-bottom: 20px;
    }

    .content-section {
        margin-top: 34px;
        margin-bottom: 18px;
    }

    .info-card {
        background: #ffffff;
        border: 1px solid #e7ebf0;
        border-radius: 16px;
        padding: 23px;
        min-height: 160px;
        box-shadow: 0 4px 14px rgba(20,35,55,0.035);
        margin-bottom: 12px;
    }

    .info-icon {
        font-size: 25px;
        margin-bottom: 12px;
    }

    .info-title {
        font-size: 16px;
        font-weight: 800;
        color: #203447;
        margin-bottom: 8px;
    }

    .info-description {
        color: #68788a;
        font-size: 12px;
        line-height: 1.75;
    }

    .client-card {
        background: #ffffff;
        border: 1px solid #e7ebf0;
        border-radius: 15px;
        padding: 24px 18px;
        text-align: center;
        min-height: 130px;
        box-shadow: 0 4px 14px rgba(20,35,55,0.035);
        margin-bottom: 12px;
    }

    .client-name {
        color: #203447;
        font-size: 19px;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .client-caption {
        color: #778596;
        font-size: 11px;
        line-height: 1.6;
    }

    .objective-card {
        background: #ffffff;
        border-left: 4px solid #85bc4b;
        border-radius: 10px;
        padding: 17px 18px;
        margin-bottom: 12px;
        box-shadow: 0 4px 14px rgba(20,35,55,0.035);
    }

    .objective-title {
        font-size: 14px;
        font-weight: 800;
        color: #23384b;
        margin-bottom: 5px;
    }

    .objective-description {
        color: #6d7b8a;
        font-size: 12px;
        line-height: 1.7;
    }

    .stage-card {
        background: #ffffff;
        border: 1px solid #e7ebf0;
        border-radius: 15px;
        padding: 20px;
        min-height: 175px;
        margin-bottom: 12px;
    }

    .stage-number {
        color: #7dbb43;
        font-size: 12px;
        font-weight: 900;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }

    .stage-title {
        color: #203447;
        font-size: 15px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .stage-description {
        color: #6d7b8a;
        font-size: 12px;
        line-height: 1.7;
    }

    .vision-panel {
        background: #142c40;
        color: #ffffff;
        border-radius: 18px;
        padding: 28px;
        margin-top: 12px;
        margin-bottom: 25px;
    }

    .vision-title {
        color: #a7d66b;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 9px;
    }

    .vision-text {
        color: #eef4f7;
        font-size: 14px;
        line-height: 1.8;
    }

    .team-card {
        background: #ffffff;
        border: 1px solid #e7ebf0;
        border-radius: 16px;
        padding: 20px;
        min-height: 175px;
        margin-bottom: 10px;
        box-shadow: 0 4px 14px rgba(20,35,55,0.035);
    }

    .team-icon {
        font-size: 26px;
        margin-bottom: 10px;
    }

    .team-title {
        font-size: 16px;
        font-weight: 850;
        color: #203447;
        margin-bottom: 4px;
    }

    .team-subtitle {
        color: #7aa944;
        font-size: 11px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .team-description {
        color: #6d7b8a;
        font-size: 12px;
        line-height: 1.65;
        min-height: 40px;
    }

    .cta-panel {
        background: #eaf3e2;
        border: 1px solid #d9e9cb;
        border-radius: 18px;
        padding: 30px;
        margin-top: 25px;
        text-align: center;
    }

    .cta-title {
        color: #203447;
        font-size: 23px;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .cta-description {
        color: #63735b;
        font-size: 13px;
        line-height: 1.7;
        margin-bottom: 10px;
    }

    .page-heading {
        color: #1b3043;
        font-size: 30px;
        font-weight: 900;
        margin-bottom: 7px;
    }

    .page-subheading {
        color: #718092;
        font-size: 14px;
        line-height: 1.7;
        margin-bottom: 22px;
    }

    .dashboard-card {
        background: #ffffff;
        border: 1px solid #e7ebf0;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 12px;
    }

    .dashboard-card-title {
        color: #203447;
        font-size: 15px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .dashboard-card-text {
        color: #6d7b8a;
        font-size: 12px;
        line-height: 1.7;
    }

    .footer {
        border-top: 1px solid #e2e8ee;
        margin-top: 40px;
        padding: 20px 0 5px 0;
        color: #8491a0;
        font-size: 11px;
        text-align: center;
    }

    div.stButton > button {
        border-radius: 10px;
        border: 1px solid #dbe3e9;
        background: #ffffff;
        color: #203447;
        font-weight: 750;
        padding: 0.55rem 1rem;
        transition: all 0.15s ease;
    }

    div.stButton > button:hover {
        border-color: #7dbb43;
        color: #477d20;
        background: #f7fbf3;
    }

    div.stButton > button[kind="primary"] {
        background: #7dbb43;
        border: 1px solid #7dbb43;
        color: #ffffff;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #689f34;
        border-color: #689f34;
        color: #ffffff;
    }

    @media (max-width: 800px) {

        .hero {
            padding: 36px 25px;
        }

        .topbar {
            padding: 12px 14px;
        }

        .academy-name {
            letter-spacing: 1px;
            font-size: 9px;
        }

    }

    @media (max-width: 480px) {

        .hero {
            padding: 30px 20px;
        }

    }

    </style>
    """
)


# =========================================================
# TOP NAVIGATION
# =========================================================

st.html(
    """
    <div class="topbar">

        <div>

            <div class="logo-text">
                ADVANSYS <span class="logo-green">ESC</span>
            </div>

            <div class="academy-name">
                CONTROLS TRAINING ACADEMY
            </div>

        </div>

        <div class="topbar-tag">
            ENGINEERING LEARNING PLATFORM
        </div>

    </div>
    """
)


nav1, nav2, nav3, spacer = st.columns([1, 1, 1, 5])


with nav1:

    if st.button(
        "⌂  Home",
        use_container_width=True,
        key="nav_home",
    ):

        go_to("home")


with nav2:

    if st.button(
        "▦  Teams",
        use_container_width=True,
        key="nav_teams",
    ):

        if st.session_state.logged_in:
            go_to("teams")

        else:
            go_to("login")


with nav3:

    if st.button(
        "▤  Dashboard",
        use_container_width=True,
        key="nav_dashboard",
    ):

        if st.session_state.logged_in:
            go_to("dashboard")

        else:
            go_to("login")


st.html(
    "<div style='height:8px'></div>"
)


# =========================================================
# HOME PAGE
# =========================================================

if current_page == "home":

    st.html(
        """
        <div class="hero">

            <div class="hero-small">
                ADVANSYS ESC
            </div>

            <div class="hero-title">
                CONTROLS<br>
                <span>TRAINING ACADEMY</span>
            </div>

            <div class="hero-description">
                Building engineering knowledge for the next generation of
                warehouse automation professionals. Learn, explore, and
                develop your technical skills through a centralized
                learning experience.
            </div>

            <span class="hero-pill">
                Warehouse Automation
            </span>

            <span class="hero-pill">
                Controls Engineering
            </span>

            <span class="hero-pill">
                Hardware & Installation
            </span>

        </div>
        """
    )


    st.html(
        """
        <div class="content-section">

            <div class="section-kicker">
                ABOUT THE ACADEMY
            </div>

            <div class="section-title">
                Engineering the Future of Automation
            </div>

            <div class="section-description">
                Advansys ESC delivers warehouse automation solutions that
                support the movement, handling, and management of materials
                across complex facilities. The Controls Training Academy is
                designed to bring technical learning resources together,
                support engineering development, and help team members build
                a stronger understanding of automation systems and project
                workflows.
            </div>

        </div>
        """
    )


    st.html(
        """
        <div class="content-section">

            <div class="section-kicker">
                OUR CLIENTS
            </div>

            <div class="section-title">
                Supporting Global Automation Projects
            </div>

            <div class="section-description">
                Advansys ESC works on warehouse automation solutions for
                international companies and projects, including:
            </div>

        </div>
        """
    )


    client_cols = st.columns(3)


    clients = [

        (
            "Dematic",
            "Warehouse automation and material handling solutions."
        ),

        (
            "Amazon",
            "Automation systems supporting warehouse operations."
        ),

        (
            "Daifuku",
            "Material handling and automated logistics solutions."
        ),

    ]


    for col, (client_name, client_desc) in zip(
        client_cols,
        clients
    ):

        with col:

            st.html(
                f"""
                <div class="client-card">

                    <div class="client-name">
                        {client_name}
                    </div>

                    <div class="client-caption">
                        {client_desc}
                    </div>

                </div>
                """
            )


    st.html(
        """
        <div class="content-section">

            <div class="section-kicker">
                WHAT WE WORK ON
            </div>

            <div class="section-title">
                Warehouse Automation Solutions
            </div>

            <div class="section-description">
                Automation projects bring together electrical hardware,
                control systems, field devices, and engineering
                documentation to help warehouse operations run as intended.
            </div>

        </div>
        """
    )


    solution_cols = st.columns(3)


    solutions = [

        (
            "📦",
            "Conveyor Systems",
            "Material transportation systems, conveyor layouts, and the devices used to move products through a facility.",
        ),

        (
            "🔀",
            "Sorting & Routing",
            "Automated sorting and routing concepts that help direct materials through different process areas.",
        ),

        (
            "⚙️",
            "Controls & Integration",
            "Control hardware, field devices, electrical drawings, PLC interfaces, and integration between systems.",
        ),

    ]


    for col, (icon, title, description) in zip(
        solution_cols,
        solutions
    ):

        with col:

            st.html(
                f"""
                <div class="info-card">

                    <div class="info-icon">
                        {icon}
                    </div>

                    <div class="info-title">
                        {title}
                    </div>

                    <div class="info-description">
                        {description}
                    </div>

                </div>
                """
            )


    st.html(
        """
        <div class="content-section">

            <div class="section-kicker">
                ACADEMY OBJECTIVES
            </div>

            <div class="section-title">
                Learning with a Clear Purpose
            </div>

            <div class="section-description">
                The academy aims to make technical knowledge easier to access
                and to provide a consistent learning path across teams.
            </div>

        </div>
        """
    )


    objectives = [

        (
            "Accelerate Onboarding",
            "Help new team members become familiar with engineering tools, documentation, and project workflows.",
        ),

        (
            "Standardize Learning",
            "Provide shared learning materials and technical references that support consistent understanding.",
        ),

        (
            "Centralize Resources",
            "Bring documents, videos, training modules, and assessments together in one place.",
        ),

        (
            "Support Knowledge Retention",
            "Make it easier for engineers to revisit important concepts and technical information.",
        ),

        (
            "Track Learning Progress",
            "Provide a simple way to follow completed modules and learning activities.",
        ),

        (
            "Encourage Development",
            "Support continuous learning and technical growth within engineering teams.",
        ),

    ]


    obj_cols = st.columns(2)


    for i, (title, description) in enumerate(objectives):

        with obj_cols[i % 2]:

            st.html(
                f"""
                <div class="objective-card">

                    <div class="objective-title">
                        {title}
                    </div>

                    <div class="objective-description">
                        {description}
                    </div>

                </div>
                """
            )


    st.html(
        """
        <div class="content-section">

            <div class="section-kicker">
                LEARNING JOURNEY
            </div>

            <div class="section-title">
                From Fundamentals to Project Knowledge
            </div>

            <div class="section-description">
                A structured path that introduces the company and core
                concepts before moving into technical topics and
                team-focused learning.
            </div>

        </div>
        """
    )


    stages = [

        (
            "01",
            "Company Introduction",
            "Get familiar with Advansys ESC, the academy, and how engineering teams collaborate.",
        ),

        (
            "02",
            "Automation Fundamentals",
            "Explore warehouse processes, material handling, conveyors, and sorting concepts.",
        ),

        (
            "03",
            "Hardware & Installation",
            "Understand electrical drawings, power distribution, device connections, and installation references.",
        ),

        (
            "04",
            "Team Specialization",
            "Continue learning through team-related materials, project references, and technical assessments.",
        ),

    ]


    stage_cols = st.columns(4)


    for col, (number, title, description) in zip(
        stage_cols,
        stages
    ):

        with col:

            st.html(
                f"""
                <div class="stage-card">

                    <div class="stage-number">
                        STAGE {number}
                    </div>

                    <div class="stage-title">
                        {title}
                    </div>

                    <div class="stage-description">
                        {description}
                    </div>

                </div>
                """
            )


    st.html(
        """
        <div class="content-section">

            <div class="section-kicker">
                LEARNING RESOURCES
            </div>

            <div class="section-title">
                One Place for Technical Learning
            </div>

            <div class="section-description">
                The platform is structured to host different types of
                learning resources, making it easier to find and revisit
                relevant technical material.
            </div>

        </div>
        """
    )


    resource_cols = st.columns(3)


    resources = [

        (
            "📄",
            "Technical Documentation",
            "Engineering references, design documents, standards, and project-related material.",
        ),

        (
            "🎥",
            "Training Videos",
            "Visual explanations and demonstrations of technical concepts, tools, and workflows.",
        ),

        (
            "🧰",
            "Hardware Design",
            "Learning material related to electrical drawings, components, buses, and field devices.",
        ),

        (
            "🖥️",
            "PLC & Controls",
            "Introductory learning about PLC concepts, control logic, and system interfaces.",
        ),

        (
            "📝",
            "Assessments",
            "Knowledge checks and quizzes to review concepts covered in the training modules.",
        ),

        (
            "📊",
            "Progress Tracking",
            "A simple overview of completed modules and learning progress.",
        ),

    ]


    for i, (icon, title, description) in enumerate(resources):

        with resource_cols[i % 3]:

            st.html(
                f"""
                <div class="info-card">

                    <div class="info-icon">
                        {icon}
                    </div>

                    <div class="info-title">
                        {title}
                    </div>

                    <div class="info-description">
                        {description}
                    </div>

                </div>
                """
            )


    # =====================================================
    # LOGIN / REGISTER
    # =====================================================

    st.html(
        """
        <div class="content-section">

            <div class="section-kicker">
                ACCESS THE ACADEMY
            </div>

            <div class="section-title">
                Start Your Learning Journey
            </div>

            <div class="section-description">
                Sign in with your Advansys ESC account or create a new account
                using your company email address.
            </div>

        </div>
        """
    )


    auth_cols = st.columns(2)


    with auth_cols[0]:

        if st.button(
            "🔐  LOG IN",
            key="home_login",
            use_container_width=True,
            type="primary",
        ):

            go_to("login")


    with auth_cols[1]:

        if st.button(
            "📝  REGISTER",
            key="home_register",
            use_container_width=True,
        ):

            go_to("register")


    st.html(
        """
        <div class="vision-panel">

            <div class="vision-title">
                OUR VISION
            </div>

            <div class="vision-text">
                To support a culture of continuous learning, technical
                collaboration, and engineering development that contributes
                to the delivery of warehouse automation solutions.
            </div>

            <br>

            <div class="vision-title">
                OUR MISSION
            </div>

            <div class="vision-text">
                To make technical knowledge more accessible through
                structured learning resources, shared references, and
                opportunities for practical development.
            </div>

        </div>
        """
    )


    st.html(
        """
        <div class="cta-panel">

            <div class="cta-title">
                Learn. Explore. Engineer.
            </div>

            <div class="cta-description">
                Start exploring the academy and continue building your
                technical knowledge, one step at a time.
            </div>

        </div>
        """
    )


# =========================================================
# REGISTER PAGE
# =========================================================

elif current_page == "register":

    st.html(
        """
        <div class="section-kicker">
            CREATE ACCOUNT
        </div>

        <div class="page-heading">
            Register for the Academy
        </div>

        <div class="page-subheading">
            Create your Advansys ESC account using your company email address.
        </div>
        """
    )


    register_col = st.columns([1, 2, 1])[1]


    with register_col:

        with st.container(border=True):

            email = st.text_input(
                "Company Email",
                placeholder="Enter your company email",
                key="register_email",
            )

            password = st.text_input(
                "Password",
                type="password",
                key="register_password",
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="register_confirm_password",
            )


            if st.button(
                "Create Account",
                type="primary",
                use_container_width=True,
                key="register_submit",
            ):

                email = email.strip().lower()


                if not is_valid_company_email(email):

                    st.error(
                        "You must use your Advansys ESC company email."
                    )


                elif not password:

                    st.warning(
                        "Please enter a password."
                    )


                elif password != confirm_password:

                    st.error(
                        "Passwords do not match."
                    )


                else:

                    if register_user(
                        email,
                        password
                    ):

                        st.success(
                            "Registration successful! Please log in."
                        )


    if st.button(
        "← Back to Home",
        use_container_width=True,
        key="register_back",
    ):

        go_to("home")


# =========================================================
# LOGIN PAGE
# =========================================================

elif current_page == "login":

    st.html(
        """
        <div class="section-kicker">
            ACADEMY ACCESS
        </div>

        <div class="page-heading">
            Welcome Back
        </div>

        <div class="page-subheading">
            Log in using your Advansys ESC company account.
        </div>
        """
    )


    login_col = st.columns([1, 2, 1])[1]


    with login_col:

        with st.container(border=True):

            email = st.text_input(
                "Company Email",
                placeholder="Enter your company email",
                key="login_email",
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password",
            )


            if st.button(
                "Log In",
                type="primary",
                use_container_width=True,
                key="login_submit",
            ):

                email = email.strip().lower()


                if login_user(
                    email,
                    password
                ):

                    st.success(
                        "Login successful!"
                    )

                else:

                    st.error(
                        "Invalid email or password. "
                        "Please check your credentials or register first."
                    )


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    login_buttons = st.columns(2)


    with login_buttons[0]:

        if st.button(
            "Create a New Account",
            use_container_width=True,
            key="login_register",
        ):

            go_to("register")


    with login_buttons[1]:

        if st.button(
            "← Back to Home",
            use_container_width=True,
            key="login_back",
        ):

            go_to("home")


# =========================================================
# CHOOSE TEAM PAGE
# =========================================================

elif current_page == "choose_team":

    if not st.session_state.logged_in:

        go_to("login")

    st.html(
        """
        <div class="section-kicker">
            ACADEMY ACCESS
        </div>

        <div class="page-heading">
            Choose Your Team
        </div>

        <div class="page-subheading">
            Select your engineering team to access the relevant learning dashboard.
        </div>
        """
    )


    if st.session_state.current_user:

        st.caption(
            f"Logged in as: {st.session_state.current_user}"
        )


    team_cols = st.columns(2)


    for i, (team_code, team) in enumerate(
        teams.items()
    ):

        with team_cols[i % 2]:

            st.html(
                f"""
                <div class="team-card">

                    <div class="team-icon">
                        {team["icon"]}
                    </div>

                    <div class="team-title">
                        {team["name"]}
                    </div>

                    <div class="team-subtitle">
                        {team["full_name"]}
                    </div>

                    <div class="team-description">
                        {team["description"]}
                    </div>

                </div>
                """
            )


            if st.button(
                f"Continue with {team_code}",
                key=f"choose_team_{team_code}",
                use_container_width=True,
                type="primary",
            ):

                select_team(team_code)


# =========================================================
# TEAMS PAGE
# =========================================================

elif current_page == "teams":

    if not st.session_state.logged_in:

        go_to("login")

    st.html(
        """
        <div class="section-kicker">
            OUR ENGINEERING TEAMS
        </div>

        <div class="page-heading">
            Choose Your Team
        </div>

        <div class="page-subheading">
            Select a team to explore its learning dashboard and
            available training resources.
        </div>
        """
    )


    team_cols = st.columns(2)


    for i, (team_code, team) in enumerate(
        teams.items()
    ):

        with team_cols[i % 2]:

            topics_html = "<br>".join(
                "• " + topic
                for topic in team["topics"]
            )


            st.html(
                f"""
                <div class="team-card">

                    <div class="team-icon">
                        {team["icon"]}
                    </div>

                    <div class="team-title">
                        {team["name"]}
                    </div>

                    <div class="team-subtitle">
                        {team["full_name"]}
                    </div>

                    <div class="team-description">
                        {team["description"]}
                    </div>

                    <br>

                    <div class="info-description">

                        <b>Learning topics:</b><br>

                        {topics_html}

                    </div>

                </div>
                """
            )


            if st.button(
                f"Open {team_code} Dashboard",
                key=f"teams_open_{team_code}",
                use_container_width=True,
                type="primary",
            ):

                select_team(team_code)


# =========================================================
# DASHBOARD PAGE
# =========================================================

elif current_page == "dashboard":

    if not st.session_state.logged_in:

        go_to("login")


    team_code = st.session_state.selected_team

    team = teams[team_code]


    st.html(
        f"""
        <div class="section-kicker">
            TEAM LEARNING SPACE
        </div>

        <div class="page-heading">
            {team["icon"]} {team["name"]} Dashboard
        </div>

        <div class="page-subheading">
            {team["description"]}
        </div>
        """
    )


    top_cols = st.columns([3, 1])


    with top_cols[0]:

        st.markdown(
            f"**Logged in as:** {st.session_state.current_user}  \n"
            f"**Team:** {team['full_name']}  \n"
            f"**Learning path:** General controls engineering"
        )


    with top_cols[1]:

        if st.button(
            "← Back to Teams",
            use_container_width=True,
            key="dashboard_back",
        ):

            go_to("teams")


    st.divider()


    completed_count = len(
        st.session_state.completed_modules
    )

    total_modules = len(modules)

    progress = (
        completed_count / total_modules
        if total_modules
        else 0
    )


    p1, p2, p3 = st.columns(3)


    p1.metric(
        "Available Modules",
        total_modules,
    )


    p2.metric(
        "Completed Modules",
        completed_count,
    )


    p3.metric(
        "Progress",
        f"{progress * 100:.0f}%",
    )


    st.progress(progress)


    tab_docs, tab_videos, tab_quizzes, tab_progress = st.tabs(
        [
            "📄 Documents",
            "🎥 Videos",
            "📝 Quizzes",
            "📊 My Progress",
        ]
    )


    # =====================================================
    # DOCUMENTS TAB
    # =====================================================

    with tab_docs:

        st.subheader(
            "Training Modules"
        )

        st.caption(
            "Browse the learning modules assigned to this academy space. "
            "Training content can be added to each module."
        )


        for index, module in enumerate(modules):

            with st.container(border=True):

                c1, c2 = st.columns([4, 1])


                with c1:

                    st.markdown(
                        f"**{module['title']}**"
                    )

                    st.caption(
                        f"{module['category']}  •  {module['duration']}"
                    )

                    st.write(
                        module["description"]
                    )


                with c2:

                    if module["title"] in st.session_state.completed_modules:

                        st.success(
                            "Completed"
                        )

                    else:

                        if st.button(
                            "Mark Complete",
                            key=f"complete_{team_code}_{index}",
                            use_container_width=True,
                        ):

                            st.session_state.completed_modules.append(
                                module["title"]
                            )

                            st.rerun()


    # =====================================================
    # VIDEOS TAB
    # =====================================================

    with tab_videos:

        st.subheader(
            "Training Videos"
        )

        st.write(
            "Training videos can be organized here by topic, team, "
            "or engineering workflow."
        )


        video_topics = [

            (
                "Company & Academy Overview",
                "Introduction to Advansys ESC and the learning platform.",
            ),

            (
                "Warehouse Automation",
                "Fundamentals of material handling and automated warehouse systems.",
            ),

            (
                "Hardware Design",
                "Electrical design concepts, drawings, and hardware components.",
            ),

            (
                "PLC & Controls",
                "Control system fundamentals and PLC-related learning.",
            ),

        ]


        for title, description in video_topics:

            with st.container(border=True):

                st.markdown(
                    f"**🎬 {title}**"
                )

                st.caption(
                    description
                )

                st.info(
                    "No video has been attached to this topic yet. "
                    "Add a video link or file when the training material is ready."
                )


    # =====================================================
    # QUIZZES TAB
    # =====================================================

    with tab_quizzes:

        st.subheader(
            "Knowledge Check"
        )

        st.write(
            "Answer this sample question to review a basic "
            "warehouse automation concept."
        )


        answer = st.radio(
            "What is one purpose of a conveyor system in a warehouse?",
            [
                "To transport materials between process areas",
                "To replace all warehouse documentation",
                "To act as the only control system",
                "To remove the need for safety devices",
            ],
            index=None,
            key=f"quiz_answer_{team_code}",
        )


        if st.button(
            "Submit Answer",
            type="primary",
            key=f"quiz_submit_{team_code}",
        ):

            if answer is None:

                st.warning(
                    "Please select an answer first."
                )


            elif answer == "To transport materials between process areas":

                st.session_state.quiz_score = "correct"

                st.success(
                    "Correct! Conveyors transport materials between areas."
                )


            else:

                st.session_state.quiz_score = "incorrect"

                st.error(
                    "Not quite. Review the warehouse automation fundamentals."
                )


        if st.session_state.quiz_score == "correct":

            st.caption(
                "Latest quiz result: Correct"
            )


        elif st.session_state.quiz_score == "incorrect":

            st.caption(
                "Latest quiz result: Try again"
            )


    # =====================================================
    # PROGRESS TAB
    # =====================================================

    with tab_progress:

        st.subheader(
            "My Learning Progress"
        )


        st.metric(
            "Modules Completed",
            f"{completed_count} / {total_modules}",
        )


        st.progress(progress)


        if completed_count == 0:

            st.info(
                "You have not completed any modules yet. "
                "Visit the Documents tab and mark a module as complete."
            )


        else:

            st.markdown(
                "**Completed modules**"
            )


            for completed in st.session_state.completed_modules:

                st.markdown(
                    f"- ✅ {completed}"
                )


        st.caption(
            "This is a simple in-session progress demo. "
            "Progress is not saved permanently after the app session ends."
        )


# =========================================================
# FOOTER
# =========================================================

st.html(
    """
    <div class="footer">

        ADVANSYS ESC · CONTROLS TRAINING ACADEMY<br>

        Learn. Explore. Engineer.

    </div>
    """
)
