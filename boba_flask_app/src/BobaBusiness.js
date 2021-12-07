import React, { useState, useEffect } from "react";
import Toolbar from "@mui/material/Toolbar";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { AppBar, DrinkAccordion } from "./DrinkAccordions";
import { useParams } from "react-router-dom";

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
    topDrinks.length > 0 && (
      <div className="App">
        <AppBar>
          <Toolbar
            sx={{
              pr: "24px", // keep right padding when drawer closed
            }}
          >
            <Typography
              component="h1"
              variant="h6"
              color="inherit"
              noWrap
              sx={{ flexGrow: 1 }}
            >
              {businessName}
            </Typography>
          </Toolbar>
        </AppBar>
        <Box
          component="main"
          sx={{
            backgroundColor: (theme) =>
              theme.palette.mode === "light"
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: "100vh",
            overflow: "auto",
            marginTop: "100px",
          }}
        >
          {topDrinks.map((drink, i) => (
            <DrinkAccordion
              i={i}
              drink={drink}
              expanded={expanded}
              setExpanded={setExpanded}
            />
          ))}
        </Box>
      </div>
    )
  );
};
