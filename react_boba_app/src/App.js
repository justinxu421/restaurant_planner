// @ts-nocheck
import React from "react";
import { HashRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import { BobaBusinessPage } from "./Pages/BobaBusiness";
import { HomePage } from "./Pages/HomePage";
import { About } from "./Pages/About";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { Layout } from "./Components/Layout";

const theme = createTheme({
  typography: {
    fontFamily: "Sora",
    fontWeightLight: 400,
    fontWeightRegular: 500,
    fontWeightMedium: 600,
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router base="/restaurant_planner">
        <Layout>
          <Routes>
            <Route exact path="/" element={<HomePage />} />
            <Route
              exact
              path="/business/top_drinks/:businessId"
              element={<BobaBusinessPage />}
            />
            <Route exact path="/about" element={<About />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  );
}

export default App;
