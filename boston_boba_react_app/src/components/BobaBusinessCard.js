import React from "react";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardContent from "@mui/material/CardContent";
import { createTheme, IconButton, Typography, ThemeProvider } from "@mui/material";
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import { useNavigate } from "react-router-dom";

const theme = createTheme({
  typography: {
    fontFamily: 'Menlo',
    fontWeightLight: 400,
    fontWeightRegular: 500,
    fontWeightMedium: 600,
  }
});

export const BobaCard = ({ businessName }) => {
  const navigate = useNavigate();

  return (
    <div>
      <ThemeProvider theme={theme}>
        <Card>
          <CardHeader
            action={
              <IconButton onClick={() => navigate(`business/${businessName}`)}>
                <ArrowForwardIosIcon />
              </IconButton>
            }
            title={businessName}
            subheader="boba"
          />
          <CardContent>
            <Typography
              variant="body2"
              color="textSecondary"
              fontFamily="Sandbox"
            >
              {"placeholder text"}
            </Typography>
          </CardContent>
        </Card>
      </ThemeProvider>
    </div>
  );
};
