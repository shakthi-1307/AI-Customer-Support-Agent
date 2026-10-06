import { useEffect, useState } from "react";
import "./App.css";

const API = "http://localhost:8000/api";

function App() {
  const [items, setItems] = useState([]);
  const [index, setIndex] = useState(0);
  const [ratings, setRatings] = useState({
    relevance: 3,
    groundedness: 3,
    helpfulness: 3,
    reason: "",
  });
  const [status, setStatus] = useState("");

  useEffect(() => {
    fetch(`${API}/items`)
      .then((res) => res.json())
      .then((data) => {
        setItems(data);
        if (data.length) loadRatings(data[0]);
      })
      .catch(() => setStatus("Could not load examples."));
  }, []);

  function loadRatings(item) {
    setRatings({
      relevance: Number(item.human_relevance) || 3,
      groundedness: Number(item.human_groundedness) || 3,
      helpfulness: Number(item.human_helpfulness) || 3,
      reason: item.human_reason || "",
    });
    setStatus("");
  }

  function navigate(nextIndex) {
    if (nextIndex < 0 || nextIndex >= items.length) return;
    setIndex(nextIndex);
    loadRatings(items[nextIndex]);
  }

  async function saveRating() {
    setStatus("Saving...");

    try {
      const response = await fetch(`${API}/ratings/${index}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(ratings),
      });

      if (!response.ok) throw new Error("Save failed");

      const updated = [...items];
      updated[index] = {
        ...updated[index],
        human_relevance: ratings.relevance,
        human_groundedness: ratings.groundedness,
        human_helpfulness: ratings.helpfulness,
        human_reason: ratings.reason,
      };

      setItems(updated);
      setStatus("Saved successfully.");
    } catch {
      setStatus("Could not save rating.");
    }
  }

  const current = items[index];
  const completed = items.filter((item) =>
    ["human_relevance", "human_groundedness", "human_helpfulness"]
      .every((key) => item[key] !== "" && item[key] != null)
  ).length;

  if (!current) return <main className="app">Loading examples...</main>;

  return (
    <main className="app">
      <header>
        <div>
          <h1>Response Evaluation</h1>
          <p>Human assessment of AI-generated support responses</p>
        </div>
        <div className="progress">
          <strong>{completed}/{items.length}</strong>
          <span>Completed</span>
          <div className="progress-track">
            <div
              className="progress-fill"
              style={{ width: `${(completed / items.length) * 100}%` }}
            />
          </div>
        </div>
      </header>

      <section className="navigation">
        <button disabled={index === 0} onClick={() => navigate(index - 1)}>
          ← Previous
        </button>
        <span>Example {index + 1} of {items.length}</span>
        <button
          disabled={index === items.length - 1}
          onClick={() => navigate(index + 1)}
        >
          Next →
        </button>
      </section>

      <section className="conversation">
        <article>
          <h2>Customer message</h2>
          <p>{current.customer_message}</p>
        </article>
        <article>
          <h2>Generated response</h2>
          <p>{current.generated_response}</p>
        </article>
      </section>

      <section className="evaluation">
        <h2>Your ratings</h2>
        {[
          ["relevance", "Relevance", "Does it address the customer's actual message?"],
          ["groundedness", "Groundedness", "Is it supported by the available context?"],
          ["helpfulness", "Helpfulness", "Does it provide a useful answer or next step?"],
        ].map(([key, label, description]) => (
          <div className="rating-row" key={key}>
            <div>
              <strong>{label}</strong>
              <p>{description}</p>
            </div>
            <div className="scores">
              {[1, 2, 3, 4, 5].map((score) => (
                <button
                  key={score}
                  className={ratings[key] === score ? "selected" : ""}
                  onClick={() =>
                    setRatings({ ...ratings, [key]: score })
                  }
                >
                  {score}
                </button>
              ))}
            </div>
          </div>
        ))}

        <label htmlFor="reason">Comments (optional)</label>
        <textarea
          id="reason"
          value={ratings.reason}
          onChange={(e) =>
            setRatings({ ...ratings, reason: e.target.value })
          }
          placeholder="Explain your ratings or note any issues..."
        />

        <div className="actions">
          <button className="save" onClick={saveRating}>
            Save rating
          </button>
          <span>{status}</span>
        </div>
      </section>
    </main>
  );
}

export default App;