import React, { useState, useEffect } from "react";
import Typography from "@mui/material/Typography";
import { TopDrinkAccordion } from "../components/TopDrinkAccordion";
import { useParams } from "react-router-dom";
import { Container, createTheme, ThemeProvider } from "@mui/material";

const theme = createTheme({
  typography: {
    fontFamily: "Oxygen",
    fontWeightLight: 400,
    fontWeightRegular: 500,
    fontWeightMedium: 600,
  },
});

export const BobaBusinessPage = () => {
  const { businessId } = useParams();
  const [topDrinks, setTopDrinks] = useState([]);
  const [expanded, setExpanded] = useState(false);
  const [city, setCity] = useState(null);
  const [name, setName] = useState(null);
  const [state, setState] = useState(null);
  const [overallStars, setOverallStars] = useState(null);

  useEffect(() => {
    fetch(`/business/top_drinks/${businessId}`)
      .then((res) => res.json())
      .then((data) => {
        setTopDrinks(data.top_drinks);
        setCity(data.city);
        setName(data.business_name);
        setState(data.state);
        setOverallStars(data.overall_stars);
      });
  }, [businessId]);

  return (
    <Container>
      <div className="App">
        <Typography variant="h4" component="h1" gutterBottom>
          {name} Top Drinks
        </Typography>
        {city && state && overallStars && (
          <Typography>
            {city}, {state}: {overallStars} stars
          </Typography>
        )}
        <br />
        {topDrinks.map((drink, i) => (
          <ThemeProvider theme={theme}>
            <TopDrinkAccordion
              key={i}
              i={i}
              drink={drink}
              expanded={expanded}
              setExpanded={setExpanded}
            />
          </ThemeProvider>
        ))}
      </div>
    </Container>
  );
};
