import api from "./client";

export const getDirectors = async (params = {}) => {
  const response = await api.get("/directors/", { params });
  return response.data;
};

export const getDirector = async (id) => {
  const response = await api.get(`/directors/${id}/`);
  return response.data;
};
