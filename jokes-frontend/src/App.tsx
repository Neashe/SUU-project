import React, { useEffect, useState } from "react";
import { getAllJokes } from "./api/jokes";
import axios from "axios";

function App() {
  const [jokes, setJokes] = useState<any[]>([]);
  const [current, setCurrent] = useState(0);
  const [selectedRating, setSelectedRating] = useState<number | null>(null);
  const [view, setView] = useState<'jokes' | 'ranking'>("jokes");
  const [ranking, setRanking] = useState<any[]>([]);

  useEffect(() => {
    if (view === "jokes") {
      getAllJokes().then(data => setJokes(data.jokes || []));
    }
  }, [view]);

  async function postStats(jokeId: number, rating: number | null) {
    await axios.post("http://localhost:8006/stats/record", {
      joke_id: jokeId,
      rating: rating,
    });
  }

  const handleNext = async () => {
    if (joke) {
      await postStats(joke.id, selectedRating);
    }
    if (jokes.length && (current + 1) % jokes.length === 0) {
      getAllJokes().then(data => setJokes(data.jokes || []));
    }
    setCurrent((prev) => (jokes.length ? (prev + 1) % jokes.length : 0));
    setSelectedRating(null);
  };

  const handleViewRanking = async () => {
    const res = await axios.get("http://localhost:8006/ranking");
    setRanking(res.data.ranking || []);
    setView("ranking");
  };

  const handleBackToJokes = () => {
    setView("jokes");
    setCurrent(0);
    setSelectedRating(null);
  };

  const joke = jokes.length ? jokes[current] : null;

  if (view === "ranking") {
    return (
      <div style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "sans-serif" }}>
        <h1>Joke Ranking</h1>
        <button onClick={handleBackToJokes} style={{ marginBottom: 16 }}>Back to Jokes</button>
        <ol>
          {ranking.map((joke: any, idx: number) => (
            <li key={joke.id} style={{ marginBottom: 16, border: "1px solid #eee", borderRadius: 8, padding: 12 }}>
              <div style={{ fontWeight: 600 }}>{joke.joke}</div>
              {joke.image_url && (
                <img src={joke.image_url} alt="meme" width={120} style={{ display: "block", margin: "0.5rem 0" }} />
              )}
              <div>Average rating: {joke.average_rating ?? "N/A"}</div>
            </li>
          ))}
        </ol>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>Jokes</h1>
      <button onClick={handleViewRanking} style={{ marginBottom: 16 }}>View Ranking</button>
      {joke ? (
        <div style={{ border: "1px solid #eee", borderRadius: 8, padding: 16 }}>
          <p style={{ fontSize: 18 }}>{joke.joke}</p>
          {joke.image_url && (
            <img src={joke.image_url} alt="meme" width={200} style={{ display: "block", margin: "1rem 0" }} />
          )}
          <p>Rating: {joke.average_rating ?? "N/A"}</p>
          <div style={{ display: "flex", gap: 8, margin: "16px 0" }}>
            {[1, 2, 3, 4, 5].map((num) => (
              <div
                key={num}
                style={{
                  width: 40,
                  height: 40,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  border: selectedRating === num ? "2px solid #1976d2" : "1px solid #aaa",
                  borderRadius: 8,
                  cursor: "pointer",
                  background: selectedRating === num ? "#e3f2fd" : "#f9f9f9",
                  fontWeight: 600,
                  fontSize: 18,
                  userSelect: "none",
                  color: selectedRating === num ? "#1976d2" : undefined
                }}
                onClick={() => setSelectedRating(num)}
              >
                {num}
              </div>
            ))}
          </div>
          <button onClick={handleNext} style={{ marginTop: 16 }}>Next</button>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default App;
