import React, { useEffect, useState } from "react";
import { Button, Container, TextField, Typography } from "@mui/material";
import { BusinessCard } from "../Components/BusinessCard";
import LocalDrinkIcon from "@mui/icons-material/LocalDrink";
import Masonry from "react-masonry-css";
import { getHomeBusinesses, getSearchBusinesses } from "../actions/api";

export function HomePage() {
  const [businessValues, setBusinessValues] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    getHomeBusinesses.then((res) => {
      setBusinessValues(res.data.businesses);
    });
  }, []);

  const breakpoints = {
    default: 4,
    1100: 2,
    700: 1,
  };

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
            onChange={(e) => setSearchTerm(e.target.value)}
            label="Boba Business Name"
            variant="outlined"
            color="primary"
            InputProps={{
              endAdornment: (
                <Button
                  onClick={() =>
                    searchTerm
                      ? getSearchBusinesses(searchTerm).then((res) => {
                        setBusinessValues(res.data.businesses);
                      })
                      : getHomeBusinesses.then((res) => {
                        setBusinessValues(res.data.businesses);
                      })
                  }
                  type="submit"
                  color="primary"
                  variant="contained"
                  endIcon={<LocalDrinkIcon />}
                >
                  Search
                </Button>
              ),
            }}
            fullWidth
            required
          />
        </form>
        {/* </Box> */}
        <br />
        <Masonry
          breakpointCols={breakpoints}
          className="my-masonry-grid"
          columnClassName="my-masonry-grid_column"
        >
          {businessValues.map((business, id) => (
            <div key={id}>
              <BusinessCard business={business} />
            </div>
          ))}
        </Masonry>
        <br />
      </Container>
    </div>
  );
}
