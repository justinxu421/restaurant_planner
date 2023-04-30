import { Container, createTheme, ThemeProvider } from "@mui/material";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { getBusinessInfo, getTopDrinks, BusinessInfo } from "../actions/api";
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { TopDrinkAccordion } from "../Components/TopDrinkAccordion";

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
  const [businessValues, setBusinessValues] = useState<BusinessInfo>({});
  const [topDrinks, setTopDrinks] = useState([]);
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    if (businessId) {
      getBusinessInfo(businessId).then((res) => {
        setBusinessValues(res.data);
      });
    }
  }, [businessId]);

  useEffect(() => {
    if (businessId) {
      getTopDrinks(businessId).then((res) => {
        setTopDrinks(res.data.top_drinks);
      });
    }
  }, [businessId]);

  const { address, name, overall_star, review_count, city, state } = {
    ...businessValues,
  };

  return (
    <Container>
      <Box sx={{ textAlign: "left" }}>
        <Typography variant="h4" component="h1" gutterBottom>
          {name} Top Drinks
        </Typography>
        {address && city && state && overall_star && (<Typography variant="subtitle1" component="h2">
          <Box fontWeight="fontWeightMedium" display="inline">
            {address} {city}, {state}:{" "}
          </Box>
          {overall_star} stars with {review_count}
        </Typography>)}
        <Typography variant="subtitle1" component="h2"></Typography>
        <br />
        {topDrinks.map((drink, i) => {
          return (
            <ThemeProvider key={drink.drink_name} theme={theme}>
              <TopDrinkAccordion
                i={i}
                drink={drink}
                expanded={expanded}
                setExpanded={setExpanded}
              />
            </ThemeProvider>
          );
        })}
      </Box>
    </Container>
  );
};
