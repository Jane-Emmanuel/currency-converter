{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "6bb71ecb-275e-4689-963b-82b8483703d1",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import requests\n",
    "\n",
    "st.title(\"💱 Live Currency Converter\")\n",
    "\n",
    "# Free API endpoint\n",
    "API_URL = \"https://api.exchangerate.host/convert\"\n",
    "\n",
    "# User input\n",
    "amount = st.number_input(\"Enter amount:\", min_value=0.0, format=\"%.2f\")\n",
    "\n",
    "currencies = [\"USD\", \"EUR\", \"GBP\", \"NGN\", \"JPY\", \"CAD\"]\n",
    "\n",
    "from_currency = st.selectbox(\"From:\", currencies)\n",
    "to_currency = st.selectbox(\"To:\", currencies)\n",
    "\n",
    "if st.button(\"Convert\"):\n",
    "    if amount > 0:\n",
    "        try:\n",
    "            response = requests.get(API_URL, params={\n",
    "                \"from\": from_currency,\n",
    "                \"to\": to_currency,\n",
    "                \"amount\": amount\n",
    "            })\n",
    "            data = response.json()\n",
    "            converted_amount = data[\"result\"]\n",
    "\n",
    "            if converted_amount:\n",
    "                st.success(f\"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}\")\n",
    "            else:\n",
    "                st.error(\"Conversion failed. Try again later.\")\n",
    "        except Exception as e:\n",
    "            st.error(f\"Error: {e}\")\n",
    "    else:\n",
    "        st.warning(\"Please enter an amount greater than 0.\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ca6f84c2-5071-42e3-b3d8-43f27bd4952a",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "17b7ed40-1e0e-4205-8385-dcef2cab495b",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
