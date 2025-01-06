import React, { createContext, useState, useEffect } from "react";
import axios from "axios";

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [userData, setUserData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const API_URL = process.env.REACT_APP_API_URL;

  const axiosInstance = axios.create({
    baseURL: API_URL,
    withCredentials: true, 
  });

  const signup = async (userData) => {
    try {
      const response = await axiosInstance.post('/user/signup', userData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  };

  const login = async (email, password) => {
    try {
      const response = await axiosInstance.post('/user/login', { email, password }, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (response.status === 200  && response.data.user) {
        setUserData(response.data.user);
        return response;
      }
    } catch (error) {
      throw error;
    }
  };

  useEffect(() => {
    const fetchToken = async () => {
      setIsLoading(true)
      try {
        const response = await axiosInstance.get('/user/auth')
        if (response.data.user){
          setUserData(response.data.user)
        }
      } catch (error){
        console.log(error)
      } finally {
        setIsLoading(false)
      }
    }
    fetchToken()
    // the useEffect dependency linter must be disabled to prevent an infinite loop
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <UserContext.Provider
      value={{ signup, login, isLoading, userData }}
    >
      {children}
    </UserContext.Provider>
  );
};
