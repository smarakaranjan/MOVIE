import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Provider } from "react-redux";
import store from "./app/store";

import MoviesList from "./features/movies/MoviesList.jsx";
import MovieDetail from "./features/movies/MovieDetail.jsx";
import ActorsList from "./features/actors/ActorsList.jsx";
import ActorDetail from "./features/actors/ActorDetail.jsx";
import DirectorsList from "./features/directors/DirectorsList.jsx";
import DirectorDetail from "./features/directors/DirectorDetail.jsx";
import Navbar from "./components/Navbar.jsx";
import NotFound from "./components/NotFound.jsx";

import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<MoviesList />} />
          <Route path="/movies/:id" element={<MovieDetail />} />
          <Route path="/actors" element={<ActorsList />} />
          <Route path="/actors/:id" element={<ActorDetail />} />
          <Route path="/directors" element={<DirectorsList />} />
          <Route path="/directors/:id" element={<DirectorDetail />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </Provider>
  </React.StrictMode>
);
