"use client";

import { useEffect, useState } from "react";

const key = "menushift-feedback-v1";
type Note = { text: string; date: string };
const form = process.env.NEXT_PUBLIC_FEEDBACK_FORM_URL;

export default function Feedback() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [draft, setDraft] = useState("");
  const [status, setStatus] = useState("");

  useEffect(() => {
    try {
      const saved = JSON.parse(localStorage.getItem(key) ?? "[]");
      if (Array.isArray(saved)) setNotes(saved);
    } catch { setStatus("Saved feedback could not be read on this device."); }
  }, []);

  return (
    <section className="ns-explorer" id="feedback" aria-labelledby="feedback-title">
      <h2 id="feedback-title" className="ns-panel-title">Optional feedback</h2>
      {form?.startsWith("https://") ? <a className="studio-primary" href={form}>Open the team feedback form</a> :
        <p className="ns-note">Save and export notes from this browser to share with the team. Shared submissions are unavailable. Leave out contact details and patient information.</p>}
      <form onSubmit={(event) => {
        event.preventDefault();
        if (!draft.trim()) return;
        const next = [...notes, { text: draft.trim(), date: new Date().toISOString() }];
        try {
          localStorage.setItem(key, JSON.stringify(next));
          setNotes(next);
          setDraft("");
          setStatus("Feedback saved on this device.");
        } catch { setStatus("Feedback could not be saved. Copy the note before closing the page."); }
      }}>
        <label className="ns-field"><span className="ns-label">What could we improve?</span>
          <textarea rows={4} maxLength={500} required value={draft} onChange={(e) => setDraft(e.target.value)} />
        </label>
        <button className="studio-primary" type="submit">Save feedback note</button>
      </form>
      <p role="status">{status}</p>
      {notes.length > 0 && <details className="studio-disclosure">
        <summary>Review notes on this device ({notes.length})</summary>
        <ul>{notes.map((note, i) => <li key={i}>{note.text}</li>)}</ul>
        <button className="studio-secondary" onClick={() => {
          const url = URL.createObjectURL(new Blob([JSON.stringify(notes, null, 2)], { type: "application/json" }));
          const link = document.createElement("a"); link.href = url; link.download = "menushift-feedback.json"; link.click();
          setTimeout(() => URL.revokeObjectURL(url), 1000);
        }}>Export feedback notes</button>
      </details>}
    </section>
  );
}
