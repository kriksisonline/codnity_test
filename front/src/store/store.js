import { configureStore } from "@reduxjs/toolkit";
import storiesReducer from "./storySlice";

export const store = configureStore({
  reducer: {
    stories: storiesReducer,
  },
});
