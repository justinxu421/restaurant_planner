import React from "react";
import { styled } from '@mui/material/styles';
import ArrowForwardIosSharpIcon from '@mui/icons-material/ArrowForwardIosSharp';
import Rating from '@mui/material/Rating';
import MuiAccordion from '@mui/material/Accordion';
import MuiAccordionSummary from '@mui/material/AccordionSummary';
import MuiAccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';

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
    {...props} />
))(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark'
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

export const DrinkAccordion = ({ i, drink, expanded, setExpanded }) => {
  // helps deal with logic of only opening one at a time
  const handleChange = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
  };

  return (
    <Accordion
      expanded={expanded === `panel${i}`}
      onChange={handleChange(`panel${i}`)}
    >
      <AccordionSummary
        aria-controls={`panel${i}d-content`}
        id={`panel${i}d-header`}
      >
        <Typography>
          <b>{drink.drink_name}</b>, Score: {drink.score}
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
