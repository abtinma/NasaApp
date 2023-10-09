import {
  getAuth,
  onAuthStateChanged,
  GoogleAuthProvider,
  signInWithPopup,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
} from "firebase/auth";
import type { Readable } from "svelte/store";
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
import type { User as AuthUser } from "firebase/auth";
import type { Project, User } from "$lib/types.ts";
import { initializeApp } from "firebase/app";
import { writable, derived, get } from "svelte/store";
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
    const { subscribe } = writable<AuthUser | null>(null);
    return {
      subscribe,
    };
  }

  const { subscribe } = writable<AuthUser | null>(
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

export function docStore<T>(path: string) {
  let unsubscribe: () => void;
  const docRef = doc(db, path);

  const { subscribe } = writable<{ data: T | null; status: boolean | null }>(
    { data: null, status: null },
    (startSet) => {
      unsubscribe = onSnapshot(docRef, (snapshot) => {
        const exists = snapshot.exists();
        if (exists) {
          startSet({ data: (snapshot.data() as T) ?? null, status: true });
        } else {
          startSet({ data: null, status: false });
        }
      });
      return () => unsubscribe();
    }
  );

  return {
    subscribe,
    ref: docRef,
    id: docRef.id,
  };
}

export const thisUser: Readable<User | null | undefined> = derived(
  user,
  ($user, set) => {
    if ($user) {
      return docStore<User>(`users/${$user.uid}`).subscribe(
        ({ data, status }) => {
          if (status === true) {
            set(data);
          } else if (status === false) {
            set(null);
          }
        }
      );
    } else {
      set(undefined);
    }
  }
);

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

  const uploadProjects = async () => {
    for (const project of projects) {
      await setDoc(doc(db, "projects", project.project_id), project);
    }
  };

  const uploadToFirestore = async () => {
    await uploadUsers();
    await uploadProjects();
    console.log("Upload completed.");
  };

  uploadToFirestore().catch((error) => {
    console.error("Error uploading data:", error);
  });
}

export async function readProjects(fetchLimit = 25) {
  const projectCollection = collection(db, "projects");
  let projectQuery = query(projectCollection, limit(fetchLimit));

  const projectSnapshot = await getDocs(projectQuery);

  const projectList = projectSnapshot.docs.map((doc) => doc.data());
  console.log(projectList);
  return projectList;
}

export async function readProjectDetails(id: string): Promise<Project | null> {
  const projectRef = doc(db, "projects", id);
  const projectSnapshot = await getDoc(projectRef);

  if (projectSnapshot.exists()) {
    return projectSnapshot.data() as Project;
  } else {
    console.log("No such document!");
    return null;
  }
}

export async function readUserDetails(id: string): Promise<User | null> {
  const userRef = doc(db, "users", id);
  const userSnapshot = await getDoc(userRef);

  if (userSnapshot.exists()) {
    return userSnapshot.data() as User;
  } else {
    return null;
  }
}

export async function addKeywordsToUserDocument(keywords: string[]) {
  const userData = get(thisUser);
  const userRef = get(user);

  if (!userData || !userRef) {
    console.warn("No user data or user ref");
    return;
  }
  const userDoc = doc(db, "users", userRef?.uid);

  let userKeywordsMap = userData?.keywordsMap || {};

  keywords.forEach((keyword: string) => {
    if (userKeywordsMap[keyword] || userKeywordsMap[keyword] === 0) {
      userKeywordsMap[keyword] = Math.min(userKeywordsMap[keyword] + 1, 10);
    } else {
      userKeywordsMap[keyword] = 0;
    }
  });
  await updateDoc(userDoc, {
    keywordsMap: userKeywordsMap,
  });
}

export async function resetKeywordsMap() {
  const userData = get(thisUser);
  const userRef = get(user);

  if (!userData || !userRef) {
    console.warn("No user data or user ref");
    return;
  }
  const userDoc = doc(db, "users", userRef?.uid);

  await updateDoc(userDoc, {
    keywordsMap: {},
  });
}

export async function getProjectsBasedOnKeyword(keywordsWithWeights) {
  if (keywordsWithWeights.length === 0) {
    return await readProjects(20);
  }
  let aggregatedResults = [];
  let uniqueProjectIds = new Set();
  let queriedKeywords = [];

  const queryPromises = [];

  for (const [keyword, weight] of keywordsWithWeights) {
    queriedKeywords.push(keyword);

    const q = query(
      collection(db, "projects"),
      where("extracted_keywords", "array-contains", keyword),
      limit(weight == 0 ? 1 : weight)
    );

    const promise = getDocs(q).then((querySnapshot) => {
      querySnapshot.docs.forEach((doc) => {
        const data = doc.data();
        const projectId = doc.id;

        if (!uniqueProjectIds.has(projectId)) {
          uniqueProjectIds.add(projectId);
          aggregatedResults.push(data);
        }
      });
    });

    queryPromises.push(promise);
  }

  await Promise.all(queryPromises);

  if (aggregatedResults.length < 20) {
    const additionalLimit = 20 - aggregatedResults.length;
    const additionalQuery = query(
      collection(db, "projects"),
      where("extracted_keywords", "not-in", queriedKeywords),
      limit(additionalLimit)
    );
    const additionalSnapshot = await getDocs(additionalQuery);

    additionalSnapshot.docs.forEach((doc) => {
      const data = doc.data();
      const projectId = doc.id;

      if (!uniqueProjectIds.has(projectId)) {
        uniqueProjectIds.add(projectId);
        aggregatedResults.push(data);
      }
    });
  }

  return aggregatedResults;
}
