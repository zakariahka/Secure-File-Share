"use client";

import { useRouter } from 'next/navigation';
import axiosInstance from '../../utils/axiosInstance';
import { useState } from 'react';

export default function Login() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      const response = await axiosInstance.post('user/login', { email, password });
      console.log("Login response:", response);  
      router.push('/main');
    } catch (error) {
      console.error("Login failed:", error);
      setError("Login failed. Please try again.");
    }
  };

  const handleToSignup = () =>{
    router.push('/signup')
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-light-pink-orange">
      <div className="p-14 bg-white rounded-lg shadow-xl space-y-6 max-w-2xl w-full mx-4">
        <h1 className="text-xl font-bold text-words-pink-orange">Login</h1>
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border-2 focus:outline-none focus:border-dark-pink-orange border-light-pink-orange bg-gray-50 h-10 px-5 rounded-lg text-sm w-full placeholder-gray-500"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border-2 focus:outline-none focus:border-dark-pink-orange border-light-pink-orange bg-gray-50 h-10 px-5 rounded-lg text-sm w-full placeholder-gray-500"
        />
        <button
          onClick={handleLogin}
          className="w-full py-2 bg-light-pink-orange text-white font-semibold rounded-lg hover:bg-dark-pink-orange transition duration-200"
        >
          Log In
        </button>
        <p>Don't have an account? <button className="text-blue-500 hover:text-blue-700" onClick={handleToSignup}>Sign up</button></p>
      </div>
    </div>
  );
}