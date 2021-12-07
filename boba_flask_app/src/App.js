import React from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import "./App.css";
import { BobaBusiness } from "./BobaBusiness";

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route
          exact
          path="/business/:businessName"
          element={<BobaBusiness />}
        />
        <Route exact path="/about" element={<About />} />
        <Route exact path="/users" element={<Users />} />
      </Routes>
    </Router>
  );
}

function Home() {
  return <h2>Home</h2>;
}

function About() {
  return <h2>About</h2>;
}

function Users() {
  return <h2>Users</h2>;
}

export default App;
