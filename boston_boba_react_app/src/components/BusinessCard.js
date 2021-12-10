import React from "react";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardContent from "@mui/material/CardContent";
import { createTheme, IconButton, Typography, ThemeProvider, Rating } from "@mui/material";
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import { useNavigate } from "react-router-dom";

const theme = createTheme({
  typography: {
    fontFamily: 'Oxygen',
    fontWeightLight: 400,
    fontWeightRegular: 500,
    fontWeightMedium: 600,
  }
});

export const BusinessCard = ({
  businessId,
  businessName,
  businessCity,
  businessState,
  businessStars,
}) => {
  const navigate = useNavigate();

  return (
    <div>
      <ThemeProvider theme={theme}>
        <Card>
          <CardHeader
            action={
              <IconButton
                onClick={() => navigate(`business/top_drinks/${businessId}`)}
              >
                <ArrowForwardIosIcon />
              </IconButton>
            }
            title={businessName}
            subheader={`${businessCity}, ${businessState}`}
          />
          <CardContent>
            <Rating name="read-only" value={businessStars} readOnly precision={0.5} />
            <Typography variant="body2" color="textSecondary">
              {`placeholder text ${businessStars}`}
            </Typography>
          </CardContent>
        </Card>
      </ThemeProvider>
    </div>
  );
};
