import React from "react";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardContent from "@mui/material/CardContent";
import {
  createTheme,
  IconButton,
  Typography,
  ThemeProvider,
  Rating,
  CardActionArea,
} from "@mui/material";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import { useNavigate } from "react-router-dom";

const theme = createTheme({
  typography: {
    fontFamily: "Oxygen",
    fontWeightLight: 400,
    fontWeightRegular: 500,
    fontWeightMedium: 600,
  },
});

export const BusinessCard = ({ business }) => {
  const navigate = useNavigate();
  const {
    business_id: id,
    name,
    city,
    state,
    address,
    overall_star,
    review_count,
  } = business;

  return (
    <div>
      <ThemeProvider theme={theme}>
        <Card>
          <CardActionArea onClick={() => navigate(`business/top_drinks/${id}`)}>
            <CardHeader
              action={
                <IconButton
                  onClick={() => navigate(`business/top_drinks/${id}`)}
                >
                  <ArrowForwardIosIcon />
                </IconButton>
              }
              title={name}
              subheader={`${city}, ${state}`}
            />
            <CardContent>
              <Typography variant="body2" color="textSecondary">
                {`The Address is ${address}`}
                <br />
                {`The number of reviews is ${review_count}`}
              </Typography>
              <br />
              <Rating
                name="read-only"
                value={overall_star}
                readOnly
                precision={0.5}
              />
            </CardContent>
          </CardActionArea>
        </Card>
      </ThemeProvider>
    </div>
  );
};
