// @ts-nocheck
import React, { useState, useEffect } from "react";
import Typography from "@mui/material/Typography";
import Box from '@mui/material/Box';
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
  const [businessValues, setBusinessValues] = useState();
  const [topDrinks, setTopDrinks] = useState([]);
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    fetch(`/business/${businessId}/info`)
      .then((res) => res.json())
      .then((data) => {
        setBusinessValues(data);
      });
  }, [businessId]);

  useEffect(() => {
    fetch(`/business/${businessId}/top_drinks`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data.top_drinks);
        setTopDrinks(data.top_drinks);
      });
  }, [businessId]);

  const {
    address,
    name,
    overall_star,
    review_count,
    city,
    state,
  } = { ...businessValues };

  return (
    <Container>
      <div className="App">
        <Typography variant="h4" component="h1" gutterBottom>
          {name} Top Drinks
        </Typography>
        <Typography variant="subtitle1" component="h2">
          <Box fontWeight='fontWeightMedium' display='inline'>
            {address} {city}, {state}:
          </Box> {' '} {overall_star} stars with {review_count} reviews
        </Typography>
        {/* <Typography variant="subtitle1" component="h2" >
        </Typography> */}
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
