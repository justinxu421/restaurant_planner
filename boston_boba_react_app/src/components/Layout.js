import HomeIcon from "@mui/icons-material/Home";
import InfoIcon from '@mui/icons-material/Info';
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Typography,
} from "@mui/material";
import { makeStyles } from "@mui/styles";
import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

const drawerWidth = 200;
const useStyles = makeStyles((theme) => {
  return {
    page: {
      background: "#f9f9f9",
      width: "100%",
      // @ts-ignore
      padding: theme.spacing(3),
    },
    drawer: {
      width: drawerWidth,
    },
    drawerPaper: {
      width: drawerWidth,
    },
    root: {
      display: "flex",
    },
    active: {
      backgroundColor: "#f4f4f4",
    },
    title: {
      // @ts-ignore
      padding: theme.spacing(2),
    },
  };
});

export const Layout = ({ children }) => {
  const classes = useStyles();
  const navigate = useNavigate();
  const location = useLocation();
  console.log(location.pathname);

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
    <div className={classes.root}>
      {/* side drawer */}
      <Drawer
        className={classes.drawer}
        variant="permanent"
        anchor="left"
        classes={{ paper: classes.drawerPaper }}
      >
        <div>
          <Typography variant="h5" className={classes.title}>Boston Boba</Typography>
        </div>

        {/* list / links */}
        <List>
          {menuItems.map((item) => (
            <div
              className={
                location.pathname === item.path ? classes.active : null
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
            </div>
          ))}
        </List>
      </Drawer>
      <div className={classes.page}>{children}</div>
    </div>
  );
};
