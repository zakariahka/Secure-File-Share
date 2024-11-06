"use client";

import { useRouter } from 'next/navigation';
import axiosInstance from '../../utils/axiosInstance';
import { useState } from 'react';
import axios, { AxiosError } from 'axios'

export default function Signup() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [confirmedPassword, setConfirmedPassword] = useState('');
  const [error, setError] = useState('');
  const [passwordMatchError, setPasswordMatchError] = useState('');

  const handleSignup = async () => {
    if (confirmedPassword && password !== confirmedPassword) {
      setPasswordMatchError("Passwords don't match.");
      return;
    }

    try {
      const response = await axiosInstance.post('user/signup', { email, name, password, confirmedPassword });
      console.log("Signup response:", response);  
      router.push('/login');
    } catch (error) {
      if (axios.isAxiosError(error)){
        console.error("Signup failed:", error.response?.data?.error);
        setError(`Signup failed. ${error.response?.data?.error || "An unexpected error occured"}`);
      }else{
        console.error("Signup failed:", error);
        setError("Signup failed. Please try again");
      }

    }
  };

  const handleConfirmedPasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setConfirmedPassword(e.target.value);
    if (password === e.target.value) {
      setPasswordMatchError('');
    }
  };

  const handleToLogin = () => {
    router.push('/login')
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-light-pink-orange">
      <div className="p-14 bg-white rounded-lg shadow-xl space-y-6 max-w-2xl w-full mx-4">
        <h1 className="text-xl font-bold text-words-pink-orange">Sign up</h1>
        {error && <p className="text-red-500 text-sm">{error}</p>}

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border-2 focus:outline-none focus:border-dark-pink-orange border-light-pink-orange bg-gray-50 h-10 px-5 rounded-lg text-sm w-full placeholder-gray-500"
        />

        <input
          type="name"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="border-2 focus:outline-none focus:border-dark-pink-orange border-light-pink-orange bg-gray-50 h-10 px-5 rounded-lg text-sm w-full placeholder-gray-500"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border-2 focus:outline-none focus:border-dark-pink-orange border-light-pink-orange bg-gray-50 h-10 px-5 rounded-lg text-sm w-full placeholder-gray-500"
        />

        <input
          type="password"
          placeholder="Confirm Password"
          value={confirmedPassword}
          onChange={handleConfirmedPasswordChange}
          className={`border-2 h-10 px-5 rounded-lg text-sm w-full placeholder-gray-500 
            ${passwordMatchError ? 'border-red-500' : 'border-light-pink-orange'} 
            focus:outline-none focus:border-${passwordMatchError ? 'red-500' : 'dark-pink-orange'}`}
        />
        {passwordMatchError && (
          <p className="text-red-500 text-sm mt-1">{passwordMatchError}</p>
        )}

        <button
          onClick={handleSignup}
          className="w-full py-2 bg-light-pink-orange text-white font-semibold rounded-lg hover:bg-dark-pink-orange transition duration-200"
        >
          Signup
        </button>
        <p>Already have an account? <button className="text-blue-500 hover:text-blue-700" onClick={handleToLogin}>Log In</button></p>
      </div>
    </div>
  );
}
