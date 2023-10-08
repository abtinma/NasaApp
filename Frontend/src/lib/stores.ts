import { writable } from "svelte/store";
import { goto } from "$app/navigation";

export const scrollY = writable(0);

const initialState = {
  history: [],
  currentIndex: -1,
};
export const historyStore = writable(initialState);

export function navigateBack() {
  historyStore.update((state) => {
    if (state.currentIndex > 0) {
      state.currentIndex--;
      goto(state.history[state.currentIndex]);
    }
    return state;
  });
}

export function navigateForward() {
  historyStore.update((state) => {
    if (state.currentIndex < state.history.length - 1) {
      state.currentIndex++;
      goto(state.history[state.currentIndex]);
    }
    return state;
  });
}

export function addRouteToHistory(path) {
  historyStore.update((state) => {
    if (state.history[state.currentIndex] !== path) {
      state.history = state.history.slice(0, state.currentIndex + 1);
      state.history.push(path);
      state.currentIndex++;
    }
    return state;
  });
}
