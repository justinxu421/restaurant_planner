// @ts-nocheck
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import { BobaBusiness } from "./pages/BobaBusiness";
import { HomePage } from "./pages/HomePage";
import { About } from 'pages/About';
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { Layout } from "components/Layout";

const theme = createTheme({
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
            <Route exact path="/" element={<HomePage />} />
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

export default App;
