'use client'
import { useRouter } from "next/navigation";
import SignInForm from "../components/SignInForm";

export default function SignInPage() {
  const router = useRouter()
  const handleSignIn = (data: { email: string; password: string; rememberMe: boolean }) => {
    console.log("Sign in data:", data);
    // Send `data` to your backend API here
    alert("Sign in submitted! Check console for details.");
    router.push('/sign-up/connect-wallet')
  };

  const handleForgotPassword = () => alert("Forgot password clicked!");
  const handleCreateAccount = () => alert("Create account clicked!");

  return (
    <SignInForm
      onSubmit={handleSignIn}
      onForgotPassword={handleForgotPassword}
      onCreateAccount={handleCreateAccount}
    />
  );
}
