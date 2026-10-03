# =========================================================
# TOP BAR
# =========================================================

top_left, top_middle, top_right = st.columns(
    [4, 3, 2],
    vertical_alignment="center"
)

# =========================================================
# LEFT — LOGO
# =========================================================

with top_left:

    st.markdown(
        """
        <div style="
            background:#ffffff;
            border:1px solid #e7ebf0;
            border-radius:14px;
            padding:14px 22px;
            box-shadow:0 4px 16px rgba(20,35,55,0.04);
            min-height:72px;
            display:flex;
            flex-direction:column;
            justify-content:center;
        ">

            <div class="logo-text">
                ADVANSYS <span class="logo-green">ESC</span>
            </div>

            <div class="academy-name">
                CONTROLS TRAINING ACADEMY
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# MIDDLE — PLATFORM TAG
# =========================================================

with top_middle:

    st.markdown(
        """
        <div style="
            min-height:72px;
            display:flex;
            justify-content:center;
            align-items:center;
        ">

            <div class="topbar-tag">
                ENGINEERING LEARNING PLATFORM
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# RIGHT — ACCOUNT
# =========================================================

with top_right:

    if st.session_state.logged_in:

        display_name = get_display_name(
            st.session_state.current_user
        )

        profile_popup = st.popover(
            f"👤  {display_name}",
            use_container_width=True,
        )

        with profile_popup:

            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    padding:4px 0 10px 0;
                ">

                    <div style="
                        font-size:28px;
                        margin-bottom:5px;
                    ">
                        👤
                    </div>

                    <div style="
                        color:#203447;
                        font-size:16px;
                        font-weight:800;
                    ">
                        {display_name}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

            st.caption(
                st.session_state.current_user
            )

            st.divider()

            uploaded_file = st.file_uploader(
                "Upload Profile Picture",
                type=[
                    "png",
                    "jpg",
                    "jpeg",
                ],
                key="profile_upload",
            )

            if uploaded_file is not None:

                save_profile_image(
                    uploaded_file
                )

                st.success(
                    "Profile picture uploaded."
                )

            if st.session_state.profile_image:

                st.image(
                    st.session_state.profile_image,
                    width=100,
                )

            st.divider()

            if st.button(
                "Sign Out",
                use_container_width=True,
                key="top_signout",
            ):

                sign_out()
                st.rerun()

    else:

        st.markdown(
            """
            <div style="
                min-height:72px;
            ">
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# NAVIGATION
# =========================================================

nav1, nav2, nav3, spacer = st.columns(
    [1, 1, 1, 5]
)

with nav1:

    if st.button(
        "⌂  Home",
        use_container_width=True,
    ):

        go_to("home")
        st.rerun()


with nav2:

    if st.button(
        "▦  Teams",
        use_container_width=True,
    ):

        if st.session_state.logged_in:
            go_to("teams")

        else:
            go_to("login")

        st.rerun()


with nav3:

    if st.button(
        "▤  Dashboard",
        use_container_width=True,
    ):

        if st.session_state.logged_in:
            go_to("dashboard")

        else:
            go_to("login")

        st.rerun()


st.markdown(
    "<div style='height:8px'></div>",
    unsafe_allow_html=True,
)
