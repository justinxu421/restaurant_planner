import React, { useState, useEffect } from "react";
import Typography from "@mui/material/Typography";
import { DrinkAccordion } from "../components/DrinkAccordions";
import { useParams } from "react-router-dom";
import { Container } from "@mui/material";

export const BobaBusiness = () => {
  const { businessName } = useParams();
  const [topDrinks, setTopDrinks] = useState([]);
  const [expanded, setExpanded] = useState(false);
  const [city, setCity] = useState(null);
  const [state, setState] = useState(null);
  const [overallStars, setOverallStars] = useState(null);

  useEffect(() => {
    fetch(`/business/${businessName}`)
      .then((res) => res.json())
      .then((data) => {
        setTopDrinks(data.top_drinks);
        setCity(data.city);
        setState(data.state);
        setOverallStars(data.overall_stars);
      });
  }, [businessName]);

  return (
    <Container>
      <div className="App">
        <Typography variant="h4" component="h1" gutterBottom>
          {businessName} Top Drinks
        </Typography>
        {city && state && overallStars && (
          <Typography>
            {city}, {state}: {overallStars} stars
          </Typography>
        )}
        <br />
        {topDrinks.map((drink, i) => (
          <DrinkAccordion
            key={i}
            i={i}
            drink={drink}
            expanded={expanded}
            setExpanded={setExpanded}
          />
        ))}
      </div>
    </Container>
  );
};