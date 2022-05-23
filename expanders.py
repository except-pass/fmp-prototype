with st.expander("⚙️ Show/Hide Installation summary plots"):
    st.markdown("These plots show data at the level of an entire installation.")
    st.markdown("This can include multiple batteries all connected in parallel")
    st.markdown("Sunspec Model 802")
    df802 = pd.read_csv('sunspec802.csv')

    gb802 = aggrid.checkbox_multiple_selection_builder(df802)
    m802_selections = aggrid.make(df802, gb802)
    m802_items = m802_selections['selected_rows']

st.write(m802_items)

with st.expander("⚙️ Show/Hide Module level plots"):
    st.markdown("These plots show data at the level of an individual battery module.")
    st.markdown("Fortress products like the eFlex are made up of a single module")
    st.markdown("Sunspec Model 805")

    df805 = pd.read_csv('sunspec805.csv')

    gb805 = aggrid.checkbox_multiple_selection_builder(df805)
    m805_selections = aggrid.make(df805, gb805)
    m805_items = m805_selections['selected_rows']

st.write(m805_items)