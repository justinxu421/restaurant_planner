import React, { useState } from "react";
import { Button, Container, Grid, TextField, Typography } from "@mui/material";
import { BobaCard } from "../components/BobaBusinessCard";
import LocalDrinkIcon from "@mui/icons-material/LocalDrink";
import Masonry from 'react-masonry-css'


export function HomePage() {
  // const [bobaBusiness, setBobaBusiness] = useState("");

  const businesses = [
    "Gong Cha",
    "Kung Fu Tea",
    "Boba Me",
    "OneZo",
    "Chatime",
    "Tsaocaa",
    "Happy Lemon Boston",
    "Chatime Quincy",
  ];

  const breakpoints = {
    default: 3,
    1100: 2, 
    700: 1
  }

  return (
    <div>
      <Container>
        <Typography
          variant="h4"
          color="textPrimary"
          component="h1"
          gutterBottom
        >
          Home Page
        </Typography>
        <form noValidate autoComplete="off">
          <TextField
            // onChange={(e) => setBobaBusiness(e.target.value)}
            label="Boba Business Name"
            variant="outlined"
            color="primary"
            fullWidth
            required
          />
        </form>
        <br />
        <Masonry
          breakpointCols={breakpoints}
          className="my-masonry-grid"
          columnClassName="my-masonry-grid_column"
        >
          {businesses.map((business, id) => (
            <div key={id}>
              <BobaCard businessName={business} />
            </div>
          ))}
        </Masonry>
        <br />
        <Button
          onClick={() => console.log("clicked")}
          type="submit"
          color="primary"
          variant="contained"
          endIcon={<LocalDrinkIcon />}
        >
          Gong Cha
        </Button>
      </Container>
    </div>
  );
}
