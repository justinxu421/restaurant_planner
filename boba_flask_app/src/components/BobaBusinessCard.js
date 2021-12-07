import React from "react";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardContent from "@mui/material/CardContent";
import { IconButton, Typography } from "@mui/material";
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import { useNavigate } from "react-router-dom";

export const BobaCard = ({ businessName }) => {
  const navigate = useNavigate();

  return (
    <div>
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
          <Typography variant="body2" color="textSecondary">
            {"placeholder text"}
          </Typography>
        </CardContent>
      </Card>
    </div>
  );
};
