import axios from "axios";

export const getHomeBusinesses = axios.get(
  process.env.REACT_APP_BACKEND_URL + `/business/home`
);

export const getSearchBusinesses = (searchTerm) =>
  axios.get(
    process.env.REACT_APP_BACKEND_URL + `/business/search/${searchTerm}`
  );

export const getBusinessInfo = (businessId) =>
  axios.get(process.env.REACT_APP_BACKEND_URL + `/business/${businessId}/info`);

export const getTopDrinks = (businessId) =>
  axios.get(
    process.env.REACT_APP_BACKEND_URL + `/business/${businessId}/top_drinks`
  );
