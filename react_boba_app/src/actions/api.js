import axios from "axios";

export const getHome = axios.get(
  process.env.REACT_APP_BACKEND_URL + `/business/home`
);

export const getBusinessInfo = (businessId) =>
  axios.get(process.env.REACT_APP_BACKEND_URL + `/business/${businessId}/info`);

export const getTopDrinks = (businessId) =>
  axios.get(
    process.env.REACT_APP_BACKEND_URL + `/business/${businessId}/top_drinks`
  );
