import axios from "axios";

const API_BASE = "http://localhost:8006"; // Frontend Gateway

export async function getAllJokes() {
  const res = await axios.get(`${API_BASE}/jokes/full`);
  return res.data;
}
