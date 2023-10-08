import {
  getAuth,
  onAuthStateChanged,
  GoogleAuthProvider,
  signInWithPopup,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
} from "firebase/auth";
import type { User } from "firebase/auth";
import { initializeApp } from "firebase/app";
import { writable, derived } from "svelte/store";

const firebaseConfig = {
  apiKey: "AIzaSyDNe7oWANjL-gpfK3qV3wW6tep2ZhhTtm8",
  authDomain: "nasaappnull.firebaseapp.com",
  projectId: "nasaappnull",
  storageBucket: "nasaappnull.appspot.com",
  messagingSenderId: "178639924116",
  appId: "1:178639924116:web:6dcdd964f5de15c4c5bd81",
  measurementId: "G-SXS58GXBB7",
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

export const provider = new GoogleAuthProvider();

function userStore() {
  let unsubscribe: () => void;

  if (!auth || !globalThis.window) {
    console.warn("Auth is not initialized or not in browser");
    const { subscribe } = writable<User | null>(null);
    return {
      subscribe,
    };
  }

  const { subscribe } = writable<User | null>(
    auth?.currentUser ?? null,
    (set) => {
      unsubscribe = onAuthStateChanged(auth, (user) => {
        console.warn(`---AUTH STATE CHANGED---`, !!user);
        set(user);
      });

      return () => unsubscribe();
    }
  );

  return {
    subscribe,
  };
}

export const user = userStore();

export function signOut() {
  auth.signOut();
}

export async function signInWithGoogle() {
  const userCredential = await signInWithPopup(auth, provider);
  if (userCredential) {
    if (userCredential._tokenResponse?.isNewUser) {
      console.warn("New user");
      
    } else {
      console.warn("Existing user");
    }
  }
}

export async function signInWithEmail(email, password) {
  try {
    const userCredential = await signInWithEmailAndPassword(
      auth,
      email,
      password
    );
    const user = userCredential.user;
    console.log("User signed in: ", user);
  } catch (error) {
    console.error("Error signing in: ", error);
  }
}

export async function signUpWithEmail(email, password) {
  try {
    const userCredential = await createUserWithEmailAndPassword(
      auth,
      email,
      password
    );
    const user = userCredential.user;
    console.log("User signed up: ", user);
  } catch (error) {
    console.error("Error signing up: ", error);
  }
}
