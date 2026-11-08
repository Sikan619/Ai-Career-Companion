import streamlit as st
import pandas as pd
from datetime import date
from utils.database import get_all_applications, update_application, delete_application, DB_TYPE
from utils.charts import create_status_pie_chart, create_timeline_chart

st.set_page_config(page_title="Dashboard | AI Career Companion", page_icon="📊", layout="wide")

# Custom page header
st.title("📊 Job Applications Dashboard")
st.caption(f"Track, manage, and analyze your job search pipeline • Storage: **{DB_TYPE}**")

# Show persistent feedback messages across page reruns
if "dashboard_msg" in st.session_state and st.session_state["dashboard_msg"]:
    msg_type, msg_text = st.session_state["dashboard_msg"]
    if msg_type == "success":
        st.success(msg_text)
    elif msg_type == "error":
        st.error(msg_text)
    st.session_state["dashboard_msg"] = None

# Fetch all applications from database
try:
    data = get_all_applications()
except Exception as e:
    st.error(f"Error fetching applications: {e}")
    data = []

if not data:
    st.info("👋 You haven't added any job applications yet. Start tracking your progress today!")
    if st.button("➕ Add Your First Application", type="primary"):
        st.switch_page("pages/2_Add_Application.py")
else:
    df = pd.DataFrame(data)

    # Standardize column names for display
    display_df = df.rename(columns={
        "id": "ID",
        "company": "Company",
        "role": "Role",
        "status": "Status",
        "applied_date": "Applied Date",
        "job_link": "Job Link",
        "notes": "Notes",
        "created_at": "Logged At"
    })

    # Summary Metrics Row
    total_apps = len(df)
    interviews = len(df[df["status"].str.lower() == "interview"])
    offers = len(df[df["status"].str.lower() == "offer"])
    rejected = len(df[df["status"].str.lower() == "rejected"])
    pending = len(df[df["status"].str.lower() == "applied"])

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📋 Total Applications", total_apps)
    col2.metric("⏳ Applied / Pending", pending)
    col3.metric("🎯 Interviews", interviews)
    col4.metric("🎉 Offers", offers)
    col5.metric("❌ Rejected", rejected)

    st.divider()

    # Visual Analytics Section
    st.subheader("📈 Pipeline Analytics")
    chart_col1, chart_col2 = st.columns([1, 1])

    with chart_col1:
        fig_pie = create_status_pie_chart(display_df)
        if fig_pie:
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.bar_chart(df["status"].value_counts())

    with chart_col2:
        fig_timeline = create_timeline_chart(display_df)
        if fig_timeline:
            st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.info("📅 Timeline chart will populate once multiple applications with valid dates are added.")

    st.divider()

    # Search and Filter Section
    st.subheader("📑 Application Records")
    f_col1, f_col2 = st.columns([2, 1])
    with f_col1:
        search_query = st.text_input("🔍 Search by Company or Role", placeholder="Type company or role name...")
    with f_col2:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Applied", "Interview", "Offer", "Rejected", "Wishlist"]
        )

    # Apply filters
    filtered_df = display_df.copy()
    if search_query.strip():
        q = search_query.strip().lower()
        filtered_df = filtered_df[
            filtered_df["Company"].str.lower().str.contains(q, na=False) |
            filtered_df["Role"].str.lower().str.contains(q, na=False)
        ]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"].str.lower() == status_filter.lower()]

    st.dataframe(
        filtered_df[["ID", "Company", "Role", "Status", "Applied Date", "Job Link", "Notes"]],
        use_container_width=True,
        hide_index=True
    )

    # 1-Click CSV Export for Reports & Presentation
    csv_bytes = filtered_df[["ID", "Company", "Role", "Status", "Applied Date", "Job Link", "Notes"]].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Applications Report (CSV)",
        data=csv_bytes,
        file_name=f"job_applications_report_{date.today().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        help="Export all filtered application records into a CSV spreadsheet."
    )

    st.divider()

    # Edit & Delete Management Section
    st.subheader("⚙️ Manage Application (Edit / Delete)")

    # Create user-friendly labels for dropdown
    app_options = {
        row["id"]: f"{row['company']} — {row['role']} (Status: {row['status']}) [ID: {row['id']}]"
        for _, row in df.iterrows()
    }
    
    selected_app_id = st.selectbox(
        "Select Application to Modify",
        options=list(app_options.keys()),
        format_func=lambda x: app_options[x]
    )

    selected_record = df[df["id"] == selected_app_id].iloc[0]

    # Two distinct tabs for Edit and Delete
    tab_edit, tab_delete = st.tabs(["✏️ Edit Application", "🗑️ Delete Application"])

    with tab_edit:
        with st.form(f"edit_form_{selected_app_id}"):
            e_col1, e_col2 = st.columns(2)
            with e_col1:
                new_company = st.text_input("Company Name *", value=selected_record["company"])
                new_role = st.text_input("Job Role *", value=selected_record["role"])
                
                statuses = ["Applied", "Interview", "Offer", "Rejected", "Wishlist"]
                curr_status = selected_record["status"]
                stat_idx = statuses.index(curr_status) if curr_status in statuses else 0
                new_status = st.selectbox("Application Status", statuses, index=stat_idx)

            with e_col2:
                # Parse existing date safely
                raw_date = selected_record.get("applied_date")
                default_date = date.today()
                if raw_date:
                    try:
                        default_date = pd.to_datetime(raw_date).date()
                    except Exception:
                        default_date = date.today()
                new_date = st.date_input("Applied Date", value=default_date)
                new_link = st.text_input("Job Link", value=selected_record.get("job_link") or "")
                new_notes = st.text_area("Notes", value=selected_record.get("notes") or "", height=85)

            submit_edit = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)

            if submit_edit:
                if not new_company.strip() or not new_role.strip():
                    st.error("Company Name and Job Role cannot be empty.")
                else:
                    try:
                        update_application(
                            selected_app_id,
                            new_company,
                            new_role,
                            new_status,
                            new_date,
                            new_link,
                            new_notes
                        )
                        st.session_state["dashboard_msg"] = ("success", f"✅ Application for '{new_company}' updated successfully!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Failed to update application: {ex}")

    with tab_delete:
        st.warning(f"Are you sure you want to delete the record for **{selected_record['company']} — {selected_record['role']}**?")
        st.caption("This action is permanent and cannot be undone.")
        
        confirm_delete = st.checkbox("I confirm that I want to delete this application record", key=f"del_chk_{selected_app_id}")
        
        if st.button("🗑️ Permanently Delete Record", type="primary", disabled=not confirm_delete):
            try:
                delete_application(selected_app_id)
                st.session_state["dashboard_msg"] = ("success", f"🗑️ Application for '{selected_record['company']}' deleted successfully.")
                st.rerun()
            except Exception as ex:
                st.error(f"Failed to delete record: {ex}")
