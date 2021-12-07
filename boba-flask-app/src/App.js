import React, { useState, useEffect } from "react";
import { styled } from '@mui/material/styles';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Box from '@mui/material/Box';
import ArrowForwardIosSharpIcon from '@mui/icons-material/ArrowForwardIosSharp';
import Rating from '@mui/material/Rating';
import MuiAccordion from '@mui/material/Accordion';
import MuiAccordionSummary from '@mui/material/AccordionSummary';
import MuiAccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';

import "./App.css";
const drawerWidth = 240;

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const Accordion = styled((props) => (
  <MuiAccordion disableGutters elevation={0} square {...props} />
))(({ theme }) => ({
  border: `1px solid ${theme.palette.divider}`,
  '&:not(:last-child)': {
    borderBottom: 0,
  },
  '&:before': {
    display: 'none',
  },
}));

const AccordionSummary = styled((props) => (
  <MuiAccordionSummary
    expandIcon={<ArrowForwardIosSharpIcon sx={{ fontSize: '0.9rem' }} />}
    {...props}
  />
))(({ theme }) => ({
  backgroundColor:
    theme.palette.mode === 'dark'
      ? 'rgba(255, 255, 255, .05)'
      : 'rgba(0, 0, 0, .03)',
  flexDirection: 'row-reverse',
  '& .MuiAccordionSummary-expandIconWrapper.Mui-expanded': {
    transform: 'rotate(90deg)',
  },
  '& .MuiAccordionSummary-content': {
    marginLeft: theme.spacing(1),
  },
}));

const AccordionDetails = styled(MuiAccordionDetails)(({ theme }) => ({
  padding: theme.spacing(2),
  borderTop: '1px solid rgba(0, 0, 0, .125)',
}));


const DrinkAccordion = ({ i, drink, expanded, setExpanded }) => {
  const handleChange = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
  };
  return (
    <Accordion
      expanded={expanded === `panel${i}`}
      onChange={handleChange(`panel${i}`)}
    >
      <AccordionSummary aria-controls={`panel${i}d-content`} id={`panel${i}d-header`}>
        <Typography>
          <b>{drink.drink_name}</b>
        </Typography>
      </AccordionSummary>
      <AccordionDetails>
        {drink.reviews.map((review, i) => (
          <div className="review" key={i}>
            <Typography>
              <b> Review {i + 1}</b>
            </Typography>
            <Typography>{review.text}</Typography>
            <Rating name="read-only" value={review.stars} readOnly />
          </div>
        ))}
      </AccordionDetails>
    </Accordion>
  );
}; 

function App() {
  const [drinks, setDrinks] = useState([]);
  const [expanded, setExpanded] = useState(false);

  const businessName = 'Tbaar'

  useEffect(() => {
    fetch(`/business/${businessName}`)
      .then((res) => res.json())
      .then((data) => {
        setDrinks(data.drinks);
      });
  }, []);
  console.log(drinks)


  return (
    drinks.length > 0 && (
      <div className="App">
        <AppBar>
          <Toolbar
            sx={{
              pr: "24px", // keep right padding when drawer closed
            }}
          >
            <Typography
              component="h1"
              variant="h6"
              color="inherit"
              noWrap
              sx={{ flexGrow: 1 }}
            >
              {businessName}
            </Typography>
          </Toolbar>
        </AppBar>
        <Box
          component="main"
          sx={{
            backgroundColor: (theme) =>
              theme.palette.mode === "light"
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: "100vh",
            overflow: "auto",
            marginTop: "100px",
          }}
        >
          {drinks.map((drink, i) => (
            <DrinkAccordion
              i={i}
              drink={drink}
              expanded={expanded}
              setExpanded={setExpanded}
            />
          ))}
        </Box>
      </div>
    )
  );
}

export default App;
