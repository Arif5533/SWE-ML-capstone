import os
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Smart Meeting Summarizer", page_icon="📝", layout="wide")

st.title("📝 Smart Meeting Summarizer & Task Generator")

with st.sidebar:
    st.header("Create Meeting")
    title = st.text_input("Meeting title", "Sprint Planning")
    transcript = st.text_area("Transcript", height=300, placeholder="Paste transcript here...")
    if st.button("Create"):
        r = requests.post(f"{API_BASE_URL}/meetings/", json={"title": title, "transcript": transcript})
        if r.ok:
            st.success(f"Created meeting #{r.json()['id']}")
        else:
            st.error(r.text)

st.subheader("Meetings")
r = requests.get(f"{API_BASE_URL}/meetings/")
if r.ok:
    meetings = r.json()
    for m in meetings:
        with st.expander(f"#{m['id']} — {m['title']}"):
            r2 = requests.get(f"{API_BASE_URL}/meetings/{m['id']}")
            if not r2.ok:
                st.error("Failed to fetch details")
                continue
            detail = r2.json()
            st.markdown("**Transcript**")
            st.code(detail["transcript"][:5000])
            if st.button(f"Analyze #{m['id']}", key=f"analyze-{m['id']}"):
                ra = requests.post(f"{API_BASE_URL}/meetings/{m['id']}/analyze")
                if ra.ok:
                    detail = ra.json()
                    st.success("Analysis complete")
                else:
                    st.error(ra.text)
            st.markdown("**Summary**")
            st.write(detail.get("summary") or "_No summary yet_")

            st.markdown("**Tasks**")
            tasks = detail.get("tasks", [])
            if not tasks:
                st.write("_No tasks yet_")
            else:
                for t in tasks:
                    st.write(f"- **{t.get('assignee') or 'Unassigned'}**: {t['description']} " +
                             (f"(Due: {t['due_date']})" if t.get("due_date") else ""))
else:
    st.error("API not reachable. Set API_BASE_URL or start backend.")
