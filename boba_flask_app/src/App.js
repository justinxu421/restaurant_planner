// @ts-nocheck
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import { BobaBusiness } from "./pages/BobaBusiness";
import { Home } from "./pages/HomePage";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { Layout } from "components/Layout";

const theme = createTheme({
  palette: {
    primary: {
      main: "#fefefe",
    },
  },
  typography: {
    fontFamily: 'Quicksand',
    fontWeightLight: 400,
    fontWeightRegular: 500,
    fontWeightMedium: 600,
  }
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Layout>
          <Routes>
            <Route exact path="/" element={<Home />} />
            <Route
              exact
              path="/business/:businessName"
              element={<BobaBusiness />}
            />
            <Route exact path="/about" element={<About />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  );
}

function About() {
  return <h2>About</h2>;
}

export default App;
