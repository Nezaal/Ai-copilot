// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth, GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDcHlgik0HWpsRNBpjHKrjItedvXkDm-ls",
  authDomain: "my-byoc-copilot-fbefc.firebaseapp.com",
  projectId: "my-byoc-copilot-fbefc",
  storageBucket: "my-byoc-copilot-fbefc.firebasestorage.app",
  messagingSenderId: "804150913656",
  appId: "1:804150913656:web:ad005702e5e9b247f71b8d",
  measurementId: "G-X2F5G5XEPP"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
// Auth exports
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

const signInWithGoogle = async () => {
  try {
    await signInWithPopup(auth, provider);
  } catch (err) {
    console.error('Google sign-in failed', err);
    throw err;
  }
};

export { auth, signInWithGoogle };