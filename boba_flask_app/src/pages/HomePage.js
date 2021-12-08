import React, { useState } from "react";
import {
  Button,
  Container,
  Grid,
  TextField,
  Typography,
} from "@mui/material";
import { BobaCard } from "../components/BobaBusinessCard";
import LocalDrinkIcon from "@mui/icons-material/LocalDrink";

export function Home() {
  const [bobaBusiness, setBobaBusiness] = useState("");
  console.log(bobaBusiness);

  const businesses = ["Gong Cha", "Kung Fu Tea", "Boba Me", "OneZo"];
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
            onChange={(e) => setBobaBusiness(e.target.value)}
            label="Boba Business Name"
            variant="outlined"
            color="primary"
            fullWidth
            required
          />
        </form>
        <br />
        <Grid container spacing={3}>
          {businesses.map((business, id) => (
            <Grid item key={id} xs={12} sm={6} md={3}>
              <BobaCard businessName={business} />
            </Grid>
          ))}
        </Grid>
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
