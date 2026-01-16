import api from "./client";

export const getGenres = async (params = {}) => {
  const response = await api.get("/genres/", { params });
  return response.data;
};
