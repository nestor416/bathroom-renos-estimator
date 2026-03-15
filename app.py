import streamlit as st

st.set_page_config(page_title="Bathroom Renos — Estimator", page_icon="🚿", layout="centered")

st.title("🚿 Bathroom Renos")
st.caption("bathroomrenos.ca · Etobicoke, Ontario")
st.divider()

# ── Client Info ──
st.subheader("Client Info")
col1, col2 = st.columns(2)
with col1:
    client_name = st.text_input("Client name", placeholder="e.g. John Smith")
with col2:
    client_address = st.text_input("Address", placeholder="123 Main St, Toronto")

job_desc = st.text_area("Scope of work", placeholder="e.g. Full ensuite — demo, tile, fixtures, vanity")

col3, col4 = st.columns(2)
with col3:
    daily_rate = st.number_input("Your daily labour rate ($)", min_value=0, value=850, step=50)
with col4:
    hst_rate = st.number_input("HST rate (%)", min_value=0.0, max_value=100.0, value=13.0, step=0.5)

st.divider()

# ── Labour Phases ──
st.subheader("Labour Phases")

if "phases" not in st.session_state:
    st.session_state.phases = [{"name": "", "days": 1.0, "override": 0.0, "use_override": False}]

for i, phase in enumerate(st.session_state.phases):
    with st.container():
        c1, c2, c3, c4, c5 = st.columns([3, 1.2, 1.2, 1.5, 0.5])
        with c1:
            st.session_state.phases[i]["name"] = st.text_input(
                "Phase description", value=phase["name"],
                placeholder="e.g. Demo, Tile, Fixtures",
                key=f"pname_{i}")
        with c2:
            st.session_state.phases[i]["days"] = st.number_input(
                "Days", min_value=0.0, value=float(phase["days"]),
                step=0.5, key=f"pdays_{i}")
        with c3:
            st.session_state.phases[i]["use_override"] = st.checkbox(
                "Fixed $", value=phase["use_override"], key=f"pchk_{i}")
        with c4:
            st.session_state.phases[i]["override"] = st.number_input(
                "Override ($)", min_value=0.0, value=float(phase["override"]),
                step=50.0, key=f"pover_{i}",
                disabled=not st.session_state.phases[i]["use_override"])
        with c5:
            st.write("")
            st.write("")
            if st.button("✕", key=f"pdel_{i}"):
                st.session_state.phases.pop(i)
                st.rerun()

if st.button("+ Add phase"):
    st.session_state.phases.append({"name": "", "days": 1.0, "override": 0.0, "use_override": False})
    st.rerun()

st.divider()

# ── Subcontractors ──
st.subheader("Subcontractors")

if "subs" not in st.session_state:
    st.session_state.subs = []

for i, sub in enumerate(st.session_state.subs):
    c1, c2, c3 = st.columns([3, 2, 0.5])
    with c1:
        st.session_state.subs[i]["name"] = st.text_input(
            "Subcontractor", value=sub["name"],
            placeholder="e.g. Electrician", key=f"sname_{i}")
    with c2:
        st.session_state.subs[i]["amount"] = st.number_input(
            "Amount ($)", min_value=0.0, value=float(sub["amount"]),
            step=50.0, key=f"samt_{i}")
    with c3:
        st.write("")
        st.write("")
        if st.button("✕", key=f"sdel_{i}"):
            st.session_state.subs.pop(i)
            st.rerun()

if st.button("+ Add subcontractor"):
    st.session_state.subs.append({"name": "", "amount": 0.0})
    st.rerun()

st.divider()

# ── Materials ──
st.subheader("Materials Allowances")

if "mats" not in st.session_state:
    st.session_state.mats = []

for i, mat in enumerate(st.session_state.mats):
    c1, c2, c3 = st.columns([3, 2, 0.5])
    with c1:
        st.session_state.mats[i]["name"] = st.text_input(
            "Item", value=mat["name"],
            placeholder="e.g. Tile allowance", key=f"mname_{i}")
    with c2:
        st.session_state.mats[i]["amount"] = st.number_input(
            "Allowance ($)", min_value=0.0, value=float(mat["amount"]),
            step=50.0, key=f"mamt_{i}")
    with c3:
        st.write("")
        st.write("")
        if st.button("✕", key=f"mdel_{i}"):
            st.session_state.mats.pop(i)
            st.rerun()

if st.button("+ Add material"):
    st.session_state.mats.append({"name": "", "amount": 0.0})
    st.rerun()

st.divider()

# ── Totals ──
labour = sum(
    p["override"] if p["use_override"] else p["days"] * daily_rate
    for p in st.session_state.phases
)
subs_total = sum(s["amount"] for s in st.session_state.subs)
mats_total = sum(m["amount"] for m in st.session_state.mats)
subtotal = labour + subs_total + mats_total
hst = subtotal * (hst_rate / 100)
total = subtotal + hst

col_a, col_b, col_c = st.columns(3)
col_a.metric("Labour", f"${labour:,.2f}")
col_b.metric("Subs + Materials", f"${subs_total + mats_total:,.2f}")
col_c.metric("Total incl. HST", f"${total:,.2f}")

st.divider()

# ── Printable Summary ──
st.subheader("Estimate Summary")

from datetime import date
today = date.today().strftime("%B %d, %Y")

summary = f"""
**BATHROOM RENOS** · bathroomrenos.ca · Etobicoke, Ontario

**Date:** {today}
**Client:** {client_name or "—"}
**Address:** {client_address or "—"}
**Scope:** {job_desc or "—"}

---

**LABOUR — PHASE BREAKDOWN**

| Phase | Days | Amount |
|---|---|---|
"""
for p in st.session_state.phases:
    amt = p["override"] if p["use_override"] else p["days"] * daily_rate
    days_label = "—" if p["use_override"] else str(p["days"])
    summary += f"| {p['name'] or '—'} | {days_label} | ${amt:,.2f} |\n"

if st.session_state.subs:
    summary += "\n**SUBCONTRACTORS**\n\n| Subcontractor | Amount |\n|---|---|\n"
    for s in st.session_state.subs:
        summary += f"| {s['name'] or '—'} | ${s['amount']:,.2f} |\n"

if st.session_state.mats:
    summary += "\n**MATERIALS ALLOWANCES**\n\n| Item | Allowance |\n|---|---|\n"
    for m in st.session_state.mats:
        summary += f"| {m['name'] or '—'} | ${m['amount']:,.2f} |\n"
