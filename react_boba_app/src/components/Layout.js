import HomeIcon from "@mui/icons-material/Home";
import InfoIcon from "@mui/icons-material/Info";
import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Typography,
} from "@mui/material";
import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

const drawerWidth = 200;

export const Layout = ({ children }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    {
      text: "Home",
      icon: <HomeIcon color="primary" />,
      path: "/",
    },
    {
      text: "About",
      icon: <InfoIcon color="primary" />,
      path: "/about",
    },
  ];
  return (
    <Box sx={{ display: "flex" }}>
      {/* side drawer */}
      <Drawer sx={{ width: drawerWidth }} variant="permanent" anchor="left">
        <div>
          <Typography variant="h5" sx={{ padding: 2 }}>
            Boston Boba
          </Typography>
        </div>

        {/* list / links */}
        <List>
          {menuItems.map((item) => (
            <Box
              sx={
                location.pathname === item.path
                  ? {
                      backgroundColor: "#f4f4f4",
                    }
                  : null
              }
            >
              <ListItem
                button
                key={item.text}
                onClick={() => navigate(item.path)}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text}> </ListItemText>
              </ListItem>
            </Box>
          ))}
        </List>
      </Drawer>
      <Box
        sx={{
          background: "#f9f9f9",
          width: "100%",
          padding: 3,
        }}
      >
        {children}
      </Box>
    </Box>
  );
};
