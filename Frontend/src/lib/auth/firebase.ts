import {
  getAuth,
  onAuthStateChanged,
  GoogleAuthProvider,
  signInWithPopup,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
} from "firebase/auth";
import {
  getFirestore,
  doc,
  getDoc,
  onSnapshot,
  collection,
  setDoc,
  getDocs,
  query,
  where,
  orderBy,
  limit,
  startAfter,
  updateDoc,
} from "firebase/firestore";
import fs from "fs";
import usersJson from "./mock_users.json";
import projectsJson from "./mock_projects.json";
import type { User } from "firebase/auth";
import { initializeApp } from "firebase/app";
import { writable, derived } from "svelte/store";
import { goto } from "$app/navigation";

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
export const db = getFirestore(app);
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
      await createUserDocument(userCredential.user.uid, {
        email: userCredential.user.email,
        keywordsMap: {},
      });
    } else {
      console.warn("Existing user");
    }
    goto("/home");
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
    goto("/home");
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
    await createUserDocument(user.uid, {
      email: user.email,
      keywordsMap: {},
    });
    goto("/home");
  } catch (error) {
    console.error("Error signing up: ", error);
  }
}

export async function createUserDocument(uid, data) {
  const userDoc = doc(db, "users", uid);
  const userSnap = await getDoc(userDoc);

  if (!userSnap.exists()) {
    await setDoc(userDoc, data);
  }
}

export async function uploadDocs() {
  const users = usersJson;
  const projects = projectsJson;

  // Function to upload users
  const uploadUsers = async () => {
    for (const user of users) {
      await setDoc(doc(db, "users", user.user_id), user);
    }
  };

  // Function to upload projects
  const uploadProjects = async () => {
    for (const project of projects) {
      await setDoc(doc(db, "projects", project.project_id), project);
    }
  };

  // Upload to Firestore
  const uploadToFirestore = async () => {
    await uploadUsers();
    await uploadProjects();
    console.log("Upload completed.");
  };

  uploadToFirestore().catch((error) => {
    console.error("Error uploading data:", error);
  });
}

let lastVisible = null;

export async function readProjects() {
  // Create a reference to the project collection
  const projectCollection = collection(db, "projects");

  // Create a query with a limit
  let projectQuery = query(projectCollection, limit(40));

  // If we have a snapshot of the last visible document, start the query after it
  if (lastVisible) {
    projectQuery = query(projectCollection, startAfter(lastVisible), limit(40));
  }

  // Execute the query
  const projectSnapshot = await getDocs(projectQuery);

  // Get the last visible document
  // lastVisible = projectSnapshot.docs[projectSnapshot.docs.length - 1];

  const projectList = projectSnapshot.docs.map((doc) => doc.data());
  console.log(projectList);
  return projectList;
}

export async function readProjectDetails(id): Project {
  const projectRef = doc(db, "projects", id);

  const projectSnapshot = await getDoc(projectRef);

  if (projectSnapshot.exists()) {
    console.log("Document data:", projectSnapshot.data());
    return projectSnapshot.data();
  } else {
    console.log("No such document!");
    return null;
  }
}

export async function readUserDetails(id): Promise<User | null> {
  const userRef = doc(db, "users", id);

  const userSnapshot = await getDoc(userRef);

  if (userSnapshot.exists()) {
    console.log("Document data:", userSnapshot.data());
    return userSnapshot.data() as User;
  } else {
    console.log("No such document!");
    return null;
  }
}

export async function addKeywordsToUserDocument(
  uid: string,
  keywords: string[]
) {
  const userDoc = doc(db, "users", uid);
  const userSnap = await getDoc(userDoc);

  if (userSnap.exists()) {
    console.warn(userSnap.data());
    let userData = userSnap.data();
    let userKeywordsMap = userData?.keywordsMap || {};

    keywords.forEach((keyword: string) => {
      if (userKeywordsMap[keyword] || userKeywordsMap[keyword] === 0) {
        userKeywordsMap[keyword]++;
      } else {
        userKeywordsMap[keyword] = 0;
      }
    });
    // Update the user document in Firestore
    await updateDoc(userDoc, {
      keywordsMap: userKeywordsMap,
    });
  }
}
