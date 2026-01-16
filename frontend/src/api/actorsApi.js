import api from "./client";

export const getActors = async (params = {}) => {
  const response = await api.get("/actors/", { params });
  return response.data;
};

export const getActor = async (id) => {
  const response = await api.get(`/actors/${id}/`);
  return response.data;
};
