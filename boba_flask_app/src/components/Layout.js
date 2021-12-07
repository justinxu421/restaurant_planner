import HomeIcon from '@mui/icons-material/Home';
import LocalDrinkIcon from "@mui/icons-material/LocalDrink";
import { Drawer, List, ListItem, ListItemIcon, ListItemText, Typography } from "@mui/material";
import { makeStyles } from "@mui/styles";
import React from "react";
import { useLocation, useNavigate } from "react-router-dom";


const drawerWidth = 200

const useStyles = makeStyles({
  page: {
    background: "#f9f9f9",
    width: "100%",
  },
  drawer: {
      width: drawerWidth,
  },
  drawerPaper: {
      width: drawerWidth,
  },
  root: {
      display: 'flex'
  },
  active: {
      background: '#f9f9f9'
  }
});
export const Layout = ({ children }) => {
  const classes = useStyles();
  const navigate = useNavigate();
  const location = useLocation();

  console.log(location.pathname === '/');
  const menuItems = [
      {
          text: 'Home',
          icon: <HomeIcon color="secondary" />,
          path: '/',
      },
      {
          text: 'Gong Cha',
          icon: <LocalDrinkIcon color="secondary" />,
          path: '/business/Gong Cha',
      },
      {
          text: 'Kung Fu Tea',
          icon: <LocalDrinkIcon color="secondary" />,
          path: '/business/Kung Fu Tea',
      }
  ]
  return (
    <div className={classes.root}>
      {/* app bar */}
      {/* side drawer */}
      <Drawer
        className={classes.drawer}
        variant="permanent"
        anchor="left"
        classes={{ paper: classes.drawerPaper }}
      >
        <div>
          <Typography variant="h5">Boston Boba</Typography>
        </div>

        {/* list / links */}
        <List>
          {menuItems.map((item) => (
            <ListItem
              button
              key={item.text}
              onClick={() => navigate(item.path)}
              className={location.pathname === item.path ? classes.active : null}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text}> </ListItemText>
            </ListItem>
          ))}
        </List>
      </Drawer>
      <div className={classes.page}>{children}</div>
    </div>
  );
};
