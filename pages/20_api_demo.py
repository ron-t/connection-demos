import csv

from urllib.parse import urljoin
import posixpath
from io import StringIO

import requests
import streamlit as st
import json

BASE_URL = "https://api-demo-for-220.onrender.com/"

with st.expander("csv demo"):
    csv_endpoint = "/csv"
    url = urljoin(BASE_URL, csv_endpoint)

    with st.form("csv_form"):
        num_rows = st.slider("How many rows to request?", 1, 100)
        num_cols = st.slider("How many columns to request?", 1, 26)

        st.write(f"Endpoint: {url}")

        csv_submitted = st.form_submit_button("Request")

    if csv_submitted:
        params = {
            "numrows": num_rows,
            "numcols": num_cols,
        }
        resp = requests.get(url, params=params)
        max_height = 100
        st.write(f"Raw request: {resp.url}")
        st.text_area("Raw response", resp.text, height=min(max_height, num_rows * 24 + 20))
        st.dataframe(csv.reader(StringIO(resp.text)))


with st.expander("Key-Value demo"):
    kv_endpoint = "/kv"
    url = urljoin(BASE_URL, kv_endpoint)

    left, right = st.columns(2)
    with left:
        with st.form("kv_get_form"):
            get_key = st.text_input("key", "key0")

            st.write(f"Endpoint: {url}")

            kv_get_submitted = st.form_submit_button("Get")

        if kv_get_submitted:
            request_endpoint = posixpath.join(kv_endpoint, get_key)
            request_url = urljoin(url, request_endpoint)
            resp = requests.get(request_url)
            st.write(f"Raw request: {resp.url}")

            st.text_area(f"Raw response (HTTP code = {resp.status_code})", resp.text)
            st.json(resp.json())

    with right:
        with st.form("kv_set_form"):
            set_key = st.text_input("key", "key0")
            value = st.text_area(f"Value")

            st.write(f"Endpoint: {url}")
            kv_set_submitted = st.form_submit_button("Set")

        if kv_set_submitted:
            request_endpoint = posixpath.join(kv_endpoint, set_key)
            request_url = urljoin(url, request_endpoint)

            resp = requests.post(request_url, json=json.loads(value))
            st.write(f"Raw request: {resp.url}")

            st.text_area(f"Raw response (HTTP code = {resp.status_code})", resp.text)
