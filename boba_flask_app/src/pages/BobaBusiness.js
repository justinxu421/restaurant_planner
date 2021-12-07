import React, { useState, useEffect } from "react";
import Typography from "@mui/material/Typography";
import { DrinkAccordion } from "./DrinkAccordions";
import { useParams } from "react-router-dom";
import { Container } from "@mui/material";

export const BobaBusiness = () => {
  const { businessName } = useParams();
  const [topDrinks, setTopDrinks] = useState([]);
  const [expanded, setExpanded] = useState(false);
  console.log(businessName);

  useEffect(() => {
    fetch(`/business/${businessName}`)
      .then((res) => res.json())
      .then((data) => {
        setTopDrinks(data.top_drinks);
      });
  }, [businessName]);
  console.log(topDrinks);

  return (
    <Container>
      <div className="App">
        <Typography
          variant="h4"
          // color="textPrimary"
          component="h1"
          gutterBottom
        >
          {businessName} Top Drinks
        </Typography>
        {topDrinks.map((drink, i) => (
          <DrinkAccordion
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
