import axios from "axios";

export const getHomeBusinesses = axios.get(
  process.env.REACT_APP_BACKEND_URL + `/business/home`
);

export const getSearchBusinesses = (searchTerm: string) =>
  axios.get(
    process.env.REACT_APP_BACKEND_URL + `/business/search/${searchTerm}`
  );

export interface BusinessInfo {
  readonly business_id: string,
  readonly name: string,
  readonly address: string,
  readonly city: string,
  readonly state: string,
  readonly overall_star: number,
  readonly review_count: number
}

export const getBusinessInfo = (businessId: string) =>
  axios.get<BusinessInfo>(process.env.REACT_APP_BACKEND_URL + `/business/${businessId}/info`);

export const getTopDrinks = (businessId: string) =>
  axios.get(
    process.env.REACT_APP_BACKEND_URL + `/business/${businessId}/top_drinks`
  );
