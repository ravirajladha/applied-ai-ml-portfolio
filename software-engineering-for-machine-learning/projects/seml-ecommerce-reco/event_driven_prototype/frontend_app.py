"""Streamlit frontend for the Event-Driven + API Gateway recommendation demo.

Deployed together with the two FastAPI services in one container. The public
recommendation flow (recommend / send-event) goes through the API GATEWAY, matching
the assignment architecture. Read-only dashboard stats are read from the internal
service running in the same container.
"""

from __future__ import annotations

import os
import time

import pandas as pd
import requests
import streamlit as st

GATEWAY = os.environ.get("GATEWAY_URL", "http://127.0.0.1:8000")
RECO = os.environ.get("RECO_SERVICE", "http://127.0.0.1:8001")
TOKEN = os.environ.get("SEML_DEMO_TOKEN", "Bearer seml-demo-token")
HEADERS = {"Authorization": TOKEN}

USERS = [f"u{i}" for i in range(1, 61)]
ITEMS = [f"P{i:02d}" for i in range(1, 41)]
ACTIONS = ["view", "click", "cart", "purchase"]

st.set_page_config(
    page_title="E-commerce Recommendation (Event-Driven + API Gateway)",
    page_icon="🛒",
    layout="wide",
)


def gw_get(path: str, **params: object) -> dict:
    response = requests.get(f"{GATEWAY}{path}", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def gw_post(path: str, body: dict) -> dict:
    response = requests.post(f"{GATEWAY}{path}", headers=HEADERS, json=body, timeout=10)
    response.raise_for_status()
    return response.json()


def reco_stats() -> dict | None:
    try:
        return requests.get(f"{RECO}/stats", timeout=5).json()
    except requests.RequestException:
        return None


def safe_image(path: str, caption: str) -> None:
    """Render an evidence image, but never let a bad/missing file crash the app."""
    if not os.path.exists(path):
        return
    try:
        st.image(path, caption=caption)
    except Exception:  # noqa: BLE001 - defensive: corrupt image should not break the page
        st.caption(f"({caption} — image unavailable)")


st.title("🛒 Real-Time Product Recommendation")
st.caption(
    "Item-based collaborative filtering · Event-Driven Architecture + API Gateway · "
    "BITS SEML Assignment I (Group G49)"
)

stats = reco_stats()
cols = st.columns(4)
if stats:
    cols[0].metric("Users", stats["users"])
    cols[1].metric("Items", stats["items"])
    cols[2].metric("Events processed", stats["events_processed"])
    cols[3].metric("Matrix density", f"{stats['matrix_density'] * 100:.1f}%")
else:
    st.warning("Backend not reachable yet — give the services a few seconds, then refresh.")

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("Get recommendations")
    st.write("Request flows through the **API Gateway** → internal `/rank` service.")
    user = st.selectbox("User", USERS, index=6)  # default u7
    k = st.slider("How many (k)", 1, 10, 5)
    if st.button("Recommend", type="primary"):
        try:
            data = gw_get("/recommend", user_id=user, k=k)
            frame = pd.DataFrame(data["recommendations"]).set_index("item_id")
            st.bar_chart(frame["score"])
            st.dataframe(frame, use_container_width=True)
            st.success(
                f"served_by = {data.get('served_by')} · pattern = {data.get('pattern')} · "
                f"strategy = {data.get('strategy')}"
            )
        except requests.RequestException as exc:
            st.error(f"Request failed: {exc}")

with right:
    st.subheader("Send an activity event")
    st.write(
        "Posted to the **API Gateway** → queued → a background consumer updates the "
        "model asynchronously (Event-Driven)."
    )
    e_user = st.selectbox("User ", USERS, index=6, key="euser")
    e_item = st.selectbox("Product", ITEMS, key="eitem")
    e_action = st.selectbox("Action", ACTIONS, index=3, key="eaction")
    if st.button("Send event"):
        try:
            result = gw_post("/activity", {"user_id": e_user, "item_id": e_item, "action": e_action})
            st.success(f"Accepted · pattern = {result.get('pattern')} · queued = {result.get('queued_events')}")
            time.sleep(0.6)
            updated = reco_stats()
            if updated:
                st.info(
                    f"Events processed is now {updated['events_processed']} — "
                    "the model updated asynchronously."
                )
        except requests.RequestException as exc:
            st.error(f"Request failed: {exc}")

st.divider()
st.subheader("Offline evaluation & evidence")
c1, c2 = st.columns(2)
with c1:
    st.metric("Offline Precision@5 (leave-3-out)", "0.323", help="From evidence/offline_metrics.json")
    safe_image("evidence/recommendation_output_plot.png", "Interaction matrix + top-5 for u7")
with c2:
    safe_image("evidence/system_architecture.png", "Event-Driven ingestion + API Gateway architecture")

st.caption(
    "Two FastAPI services (internal recommendation/event service + API gateway) and this "
    "Streamlit UI run together in one container."
)
