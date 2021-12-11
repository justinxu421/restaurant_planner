import { Container, Typography } from "@mui/material";
import React from "react";

export const About = () => {
    return (
      <Container>
        <Typography
          variant="h4"
          color="textPrimary"
          component="h1"
          gutterBottom
        >
          About
        </Typography>
        <Typography>
          This App was built by some Boba Connoisseurs, looking to streamline
          your experience for experiencing great boba
        </Typography>
      </Container>
    );
}