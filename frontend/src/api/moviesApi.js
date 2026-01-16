import api from "./client";


export const getMovies = async (params = {}) => {
  const response = await api.get("/movies/", { params });
  return response.data;
};

export const getMovie = async (id) => {
  const response = await api.get(`/movies/${id}/`);
  return response.data;
};
