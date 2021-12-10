import React, { useEffect, useState } from "react";
import { Button, Container, TextField, Typography } from "@mui/material";
import { BusinessCard } from "../components/BusinessCard";
import LocalDrinkIcon from "@mui/icons-material/LocalDrink";
import Masonry from 'react-masonry-css'


export function HomePage() {
  const [businessValues, setBusinessValues] = useState([]);

  useEffect(() => {
    fetch(`/business/home`)
      .then((res) => res.json())
      .then((data) => {
        setBusinessValues(data.businesses);
      });
  }, []);

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
          {businessValues.map((business, id) => (
            <div key={id}>
              <BusinessCard
                businessName={business.name}
                businessId={business.business_id}
                businessCity={business.city}
                businessState={business.state}
                businessStars={business.overall_star}
              />
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