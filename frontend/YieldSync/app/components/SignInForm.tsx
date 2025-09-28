"use client";
import React, { useState } from "react";
import NavBar from "../components/NavBar";

interface SignInFormProps {
  onSubmit?: (data: { email: string; password: string; rememberMe: boolean }) => void;
  onForgotPassword?: () => void;
  onCreateAccount?: () => void;
}

const SignInForm: React.FC<SignInFormProps> = ({
  onSubmit = () => {},
  onForgotPassword = () => {},
  onCreateAccount = () => {},
}) => {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ email, password, rememberMe });
  };

  return (
    <>
      <NavBar />

      <div className="min-h-[80vh] flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md bg-zinc-900/80 backdrop-blur-md -mt-6 sm:-mt-10 rounded-xl shadow-xl p-6 sm:p-8">
          {/* Header */}
          <div className="text-center mb-6">
            <h2 className="text-xl sm:text-2xl font-bold mb-1">Welcome Back</h2>
            <p className="text-xs sm:text-sm text-gray-300 ">
              Enter your credentials to access your account
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email */}
            <div className="flex flex-col">
              <label htmlFor="email" className="text-sm font-medium mb-1">
                Email address
              </label>
              <input
                id="email"
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="h-10 px-3 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400 text-sm sm:text-base"
                required
              />
            </div>

            {/* Password */}
            <div className="flex flex-col">
              <div className="flex justify-between items-center mb-1">
                <label htmlFor="password" className="text-sm font-medium">
                  Password
                </label>
                <button
                  type="button"
                  onClick={onForgotPassword}
                  className="text-xs sm:text-sm text-blue-500 hover:underline"
                >
                  Forgot password?
                </button>
              </div>
              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="h-10 w-full pr-12 px-3 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400 text-sm sm:text-base"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-xs sm:text-sm text-gray-500 hover:text-gray-700"
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>
            </div>

            {/* Remember Me */}
            <div className="flex items-center">
              <input
                id="remember"
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="h-4 w-4 rounded border-gray-300 focus:ring-blue-400"
              />
              <label
                htmlFor="remember"
                className="ml-2 text-xs sm:text-sm text-gray-300 "
              >
                Remember me
              </label>
            </div>

            {/* Submit */}
            <button
              type="submit"
              className="w-full bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 rounded-md transition-colors text-sm sm:text-base"
            >
              Sign In
            </button>
          </form>

          {/* Footer */}
          <div className="text-center mt-6 text-xs sm:text-sm text-gray-300 ">
            Don&apos;t have an account?{" "}
            <button
              onClick={onCreateAccount}
              className="text-blue-500 hover:underline font-medium"
            >
              Create account
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default SignInForm;
