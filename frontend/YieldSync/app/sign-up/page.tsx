'use client';

import { useRouter } from "next/navigation";
import { useState } from "react";
import SignInForm from "../components/SignInForm";
import { ApiClient } from "../../libs/api";

export default function SignInPage() {
  const [signPage, setSignPage] = useState(true);
  const router = useRouter();
  const apiClient = new ApiClient();

  const signup = async (data: { email: string; password: string }) => {
    const res = await apiClient.createUser({
      username: data.email.split('@')[0],
      email: data.email,
      password: data.password,
    });
    console.log("Signup response:", res);
    return res;
  };

  const signin = async (data: { email: string; password: string }) => {
    const res = await apiClient.post('/users/login', {
      email: data.email,
      password: data.password,
    });
    console.log("Signin response:", res);
    return res;
  };

  const handleSignIn = async (data: { email: string; password: string; rememberMe: boolean }) => {
    try {
      const res = signPage ? await signin(data) : await signup(data);

      if (res.access_token) {
        localStorage.setItem('token', res.access_token);
      }

      alert("Sign in successful!");
      router.push('/sign-up/connect-wallet');
    } catch (error: any) {
      alert(`Error: ${error.message}`);
    }
  };

  const handleCreateAccount = () => setSignPage(prev => !prev);

  return (
    <SignInForm
      onSubmit={handleSignIn}
      signPage={signPage}
      onCreateAccount={handleCreateAccount}
    />
  );
}
